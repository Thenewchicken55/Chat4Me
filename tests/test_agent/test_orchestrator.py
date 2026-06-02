import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from chat4me.agent.orchestrator import Orchestrator
from chat4me.config import Config
from chat4me.screen.window import WindowInfo
from chat4me.vision.analyzer import ScreenState, TextBlock


@pytest.fixture
def config():
    return Config()


@pytest.fixture
def window():
    return WindowInfo(title="Discord", left=100, top=50, width=1200, height=800)


@pytest.fixture
def orchestrator(config):
    return Orchestrator(config)


def test_orchestrator_init(orchestrator, config):
    assert orchestrator.config is config
    assert orchestrator.memory.is_empty
    assert orchestrator.state.running is False
    assert orchestrator.state.last_raw_text == ""
    assert orchestrator.state.consecutive_replies == 0


@pytest.mark.asyncio
async def test_run_stop(orchestrator):
    orchestrator._find_target_window = AsyncMock(return_value=None)
    task = asyncio.create_task(orchestrator.run())
    await asyncio.sleep(0.1)
    assert orchestrator.state.running is True
    await orchestrator.stop()
    await task
    assert orchestrator.state.running is False


@pytest.mark.asyncio
async def test_tick_no_window_found(orchestrator):
    orchestrator._find_target_window = AsyncMock(return_value=None)
    start = asyncio.get_event_loop().time()
    await orchestrator._tick()
    elapsed = asyncio.get_event_loop().time() - start
    assert elapsed >= orchestrator.config.app.poll_interval - 0.1


@pytest.mark.asyncio
async def test_tick_no_new_messages(orchestrator, window):
    orchestrator._find_target_window = AsyncMock(return_value=window)
    state = ScreenState(text_blocks=[], raw_text="existing text")
    orchestrator._capture_and_analyze = AsyncMock(return_value=state)
    orchestrator.state.last_raw_text = "existing text"
    await orchestrator._tick()
    assert orchestrator.memory.is_empty


@pytest.mark.asyncio
async def test_tick_new_message_sends_reply(orchestrator, window):
    orchestrator.state.last_raw_text = "old message"
    orchestrator._find_target_window = AsyncMock(return_value=window)
    state = ScreenState(
        text_blocks=[TextBlock(text="Hello!", left=0, top=0, width=50, height=20, confidence=95)],
        raw_text="old message\nHello!",
    )
    orchestrator._capture_and_analyze = AsyncMock(return_value=state)
    orchestrator._decide_reply = AsyncMock(return_value="Hi there!")
    orchestrator._send_reply = AsyncMock()

    await orchestrator._tick()

    assert len(orchestrator.memory) == 2
    assert orchestrator.memory.messages[0]["content"] == "Hello!"
    assert orchestrator.memory.messages[1]["content"] == "Hi there!"
    assert orchestrator.state.consecutive_replies == 1
    orchestrator._send_reply.assert_awaited_once_with("Hi there!", window)


@pytest.mark.asyncio
async def test_tick_new_message_no_reply(orchestrator, window):
    orchestrator.state.last_raw_text = "old message"
    orchestrator._find_target_window = AsyncMock(return_value=window)
    state = ScreenState(
        text_blocks=[TextBlock(text="Hello!", left=0, top=0, width=50, height=20, confidence=95)],
        raw_text="old message\nHello!",
    )
    orchestrator._capture_and_analyze = AsyncMock(return_value=state)
    orchestrator._decide_reply = AsyncMock(return_value=None)

    await orchestrator._tick()

    assert len(orchestrator.memory) == 1
    assert orchestrator.memory.messages[0]["content"] == "Hello!"
    assert orchestrator.state.consecutive_replies == 0


@pytest.mark.asyncio
async def test_tick_respects_max_consecutive_replies(orchestrator, window):
    orchestrator.state.last_raw_text = "old"
    orchestrator.state.consecutive_replies = orchestrator.config.app.max_consecutive_replies
    orchestrator._find_target_window = AsyncMock(return_value=window)
    state = ScreenState(
        text_blocks=[TextBlock(text="Hello!", left=0, top=0, width=50, height=20, confidence=95)],
        raw_text="old\nHello!",
    )
    orchestrator._capture_and_analyze = AsyncMock(return_value=state)
    orchestrator._decide_reply = AsyncMock(return_value="reply")

    await orchestrator._tick()

    assert orchestrator.state.consecutive_replies == 0
    orchestrator._decide_reply.assert_not_called()


@pytest.mark.asyncio
async def test_find_new_messages_initial(orchestrator):
    state = ScreenState(text_blocks=[], raw_text="line1\nline2")
    new = orchestrator._find_new_messages(state)
    assert new == []
    assert orchestrator.state.last_raw_text == "line1\nline2"


@pytest.mark.asyncio
async def test_find_new_messages_detects_new(orchestrator):
    orchestrator.state.last_raw_text = "line1"
    state = ScreenState(text_blocks=[], raw_text="line1\nline2\nline3")
    new = orchestrator._find_new_messages(state)
    assert new == ["line2", "line3"]


@pytest.mark.asyncio
async def test_find_new_messages_empty_current(orchestrator):
    orchestrator.state.last_raw_text = "old"
    state = ScreenState(text_blocks=[], raw_text="")
    new = orchestrator._find_new_messages(state)
    assert new == []


@patch("chat4me.agent.orchestrator.is_tesseract_available")
@pytest.mark.asyncio
async def test_orchestrator_warns_no_tesseract(mock_check, orchestrator):
    mock_check.return_value = False
    with patch("chat4me.agent.orchestrator.logger.warning") as mock_log:
        orchestrator._find_target_window = AsyncMock(return_value=None)
        task = asyncio.create_task(orchestrator.run())
        await asyncio.sleep(0.1)
        await orchestrator.stop()
        await task
        mock_log.assert_called_once()
