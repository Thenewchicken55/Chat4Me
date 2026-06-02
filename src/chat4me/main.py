from __future__ import annotations

import argparse
import asyncio
import signal
import sys

from loguru import logger
from pynput import keyboard

from chat4me.agent.orchestrator import Orchestrator
from chat4me.config import Config
from chat4me.utils.logging import setup_logging

EMERGENCY_STOP_HOTKEY = "<ctrl>+<shift>+q"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Chat4Me — local-first AI agent that chats for you in Discord",
    )
    parser.add_argument(
        "-c", "--config",
        default=None,
        help="Path to YAML config file",
    )
    parser.add_argument(
        "--target-window",
        default=None,
        help="Window title substring to monitor (overrides config)",
    )
    parser.add_argument(
        "--llm-backend",
        choices=["ollama", "openai", "anthropic"],
        default=None,
        help="LLM backend to use (overrides config)",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=None,
        help="Seconds between screen captures (overrides config)",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=None,
        help="Logging level (overrides config)",
    )
    parser.add_argument(
        "--list-windows",
        action="store_true",
        help="List visible windows and exit",
    )
    return parser.parse_args(argv)


def print_window_list() -> None:
    from chat4me.screen.window import list_windows
    titles = list_windows()
    if not titles:
        print("No visible windows found.")
        return
    print("Visible windows:")
    for t in sorted(titles):
        print(f"  {t}")


def _print_emergency_banner() -> None:
    line = "=" * 60
    print()
    print(line)
    print("  ⚠  EMERGENCY STOP  ⚠")
    print()
    print(f"  Press  {EMERGENCY_STOP_HOTKEY.upper()}  at any time")
    print("  to immediately stop the application.")
    print()
    print("  This will kill the agent, close the LLM client,")
    print("  and release all input devices.")
    print(line)
    print()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.list_windows:
        print_window_list()
        return 0

    config = Config.load(yaml_path=args.config)

    if args.target_window:
        config.app.target_window = args.target_window
    if args.llm_backend:
        config.llm.backend = args.llm_backend
    if args.poll_interval is not None:
        config.app.poll_interval = args.poll_interval
    if args.log_level:
        config.logging.level = args.log_level

    setup_logging(level=config.logging.level, log_file=config.logging.file)

    _print_emergency_banner()

    logger.info("Chat4Me starting — targeting window '{target}'", target=config.app.target_window)

    orchestrator = Orchestrator(config)

    shutdown_event = asyncio.Event()
    _hotkey_listener: keyboard.GlobalHotKeys | None = None

    def handle_signal() -> None:
        logger.info("Shutdown signal received")
        shutdown_event.set()

    def handle_emergency_stop() -> None:
        logger.error("EMERGENCY STOP triggered via hotkey ({key})", key=EMERGENCY_STOP_HOTKEY)
        shutdown_event.set()

    if sys.platform != "win32":
        loop = asyncio.new_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, handle_signal)
    else:
        loop = asyncio.new_event_loop()

    _hotkey_listener = keyboard.GlobalHotKeys({
        EMERGENCY_STOP_HOTKEY: handle_emergency_stop,
    })
    _hotkey_listener.daemon = True
    _hotkey_listener.start()

    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(asyncio.gather(
            orchestrator.run(),
            _wait_for_shutdown(shutdown_event, orchestrator),
        ))
    except KeyboardInterrupt:
        pass
    finally:
        if _hotkey_listener:
            _hotkey_listener.stop()
        loop.run_until_complete(orchestrator.stop())
        loop.close()

    logger.info("Chat4Me stopped")
    return 0


async def _wait_for_shutdown(event: asyncio.Event, orchestrator: Orchestrator) -> None:
    await event.wait()
    await orchestrator.stop()


if __name__ == "__main__":
    sys.exit(main())
