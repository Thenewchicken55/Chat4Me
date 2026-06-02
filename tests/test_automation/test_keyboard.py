from unittest.mock import MagicMock, patch

from chat4me.automation.keyboard import hotkey, press_enter, press_escape, press_key, type_and_send, type_text


@patch("chat4me.automation.keyboard.pyautogui.write")
def test_type_text(mock_write):
    type_text("hello", interval=0.1)
    mock_write.assert_called_once_with("hello", interval=0.1)


@patch("chat4me.automation.keyboard.pyautogui.write")
def test_type_text_default_interval(mock_write):
    type_text("test")
    mock_write.assert_called_once_with("test", interval=0.05)


@patch("chat4me.automation.keyboard._kbd.tap")
def test_press_enter(mock_tap):
    press_enter()
    from pynput.keyboard import Key
    mock_tap.assert_called_once_with(Key.enter)


@patch("chat4me.automation.keyboard._kbd.tap")
def test_press_escape(mock_tap):
    press_escape()
    from pynput.keyboard import Key
    mock_tap.assert_called_once_with(Key.esc)


@patch("chat4me.automation.keyboard._kbd.tap")
def test_press_key(mock_tap):
    press_key("a")
    mock_tap.assert_called_once_with("a")


@patch("chat4me.automation.keyboard.type_text")
@patch("chat4me.automation.keyboard.press_enter")
def test_type_and_send(mock_enter, mock_type):
    type_and_send("Hello!", typing_interval=0.05)
    mock_type.assert_called_once_with("Hello!", interval=0.05)
    mock_enter.assert_called_once()


@patch("chat4me.automation.keyboard.pyautogui.hotkey")
def test_hotkey(mock_hk):
    hotkey("ctrl", "c")
    mock_hk.assert_called_once_with("ctrl", "c")
