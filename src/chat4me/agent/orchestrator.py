from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from loguru import logger

from chat4me.agent.memory import ConversationMemory
from chat4me.automation.keyboard import type_and_send
from chat4me.config import Config
from chat4me.llm.client import LLMClient, create_client
from chat4me.llm.prompts import SYSTEM_PROMPT, build_chat_prompt, parse_response
from chat4me.screen.capture import capture_window, save_screenshot
from chat4me.screen.window import WindowInfo, find_window
from chat4me.vision.analyzer import ScreenState, analyze
from chat4me.vision.ocr import ocr_image_to_data, is_tesseract_available


@dataclass
class AgentState:
    last_raw_text: str = ""
    consecutive_replies: int = 0
    running: bool = False


class Orchestrator:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.memory = ConversationMemory()
        self.state = AgentState()
        self._llm: LLMClient | None = None
        self._last_window: WindowInfo | None = None

    async def _ensure_llm(self) -> LLMClient:
        if self._llm is None:
            self._llm = create_client(self.config.llm)
        return self._llm

    async def _find_target_window(self) -> WindowInfo | None:
        target = self.config.app.target_window
        window = find_window(target)
        if window is None:
            logger.warning("Window '{target}' not found", target=target)
        else:
            logger.debug("Found window: {title} at ({left},{top}) {width}x{height}", title=window.title, left=window.left, top=window.top, width=window.width, height=window.height)
        return window

    async def _capture_and_analyze(self, window: WindowInfo) -> ScreenState:
        img = capture_window(window)
        if self.config.logging.level == "DEBUG":
            save_screenshot(img, "screenshots/latest.png")
        ocr_data = ocr_image_to_data(
            img,
            lang=self.config.vision.ocr_lang,
            tesseract_cmd=self.config.vision.tesseract_cmd,
        )
        state = analyze(img, ocr_data)
        return state

    def _find_new_messages(self, state: ScreenState) -> list[str]:
        current = state.raw_text
        if not current:
            return []
        if self.state.last_raw_text == "":
            self.state.last_raw_text = current
            return []

        old_lines = set(self.state.last_raw_text.split("\n"))
        new_lines = [l for l in current.split("\n") if l and l not in old_lines]
        self.state.last_raw_text = current
        return new_lines

    async def _decide_reply(self, new_messages: list[str]) -> str | None:
        if not new_messages:
            return None

        llm = await self._ensure_llm()
        prompt_messages = build_chat_prompt(
            conversation_history=self.memory.messages,
            new_messages=new_messages,
            system_prompt=self.config.llm.system_prompt or SYSTEM_PROMPT,
        )

        response = await llm.chat(prompt_messages)
        reply = parse_response(response)
        return reply

    async def _send_reply(self, reply: str, window: WindowInfo) -> None:
        logger.info("Sending: {reply}", reply=reply[:100])
        chat_x = window.left + window.width // 2
        chat_y = window.top + window.height - 50
        from chat4me.automation.mouse import click
        click(chat_x, chat_y)
        await asyncio.sleep(0.3)
        type_and_send(reply)

    async def _tick(self) -> None:
        window = await self._find_target_window()
        if window is None:
            await asyncio.sleep(self.config.app.poll_interval)
            return

        state = await self._capture_and_analyze(window)
        new_messages = self._find_new_messages(state)

        if not new_messages:
            await asyncio.sleep(self.config.app.poll_interval)
            return

        logger.info("New messages detected: {count}", count=len(new_messages))
        for msg in new_messages:
            self.memory.add_user_message(msg)

        if self.state.consecutive_replies >= self.config.app.max_consecutive_replies:
            logger.info("Max consecutive replies reached, waiting")
            await asyncio.sleep(self.config.app.cooldown_after_reply * 2)
            self.state.consecutive_replies = 0
            return

        reply = await self._decide_reply(new_messages)
        if reply:
            await self._send_reply(reply, window)
            self.memory.add_assistant_message(reply)
            self.state.consecutive_replies += 1
            await asyncio.sleep(self.config.app.cooldown_after_reply)
        else:
            await asyncio.sleep(self.config.app.poll_interval)

    async def run(self) -> None:
        self.state.running = True
        logger.info("Orchestrator started — polling for window '{target}'", target=self.config.app.target_window)

        if not is_tesseract_available(self.config.vision.tesseract_cmd):
            logger.warning("Tesseract not found — OCR will fail. Install it or set vision.tesseract_cmd")

        while self.state.running:
            try:
                await self._tick()
            except Exception:
                logger.exception("Error in orchestrator tick")
                await asyncio.sleep(self.config.app.poll_interval * 2)

    async def stop(self) -> None:
        self.state.running = False
        if self._llm:
            await self._llm.close()
        logger.info("Orchestrator stopped")
