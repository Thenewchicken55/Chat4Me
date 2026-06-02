from unittest.mock import MagicMock, patch

from chat4me.automation.mouse import click, click_center, double_click, get_position, move_to, scroll


@patch("chat4me.automation.mouse.pyautogui.click")
def test_click(mock_click):
    click(100, 200)
    mock_click.assert_called_once_with(x=100, y=200, button="left", clicks=1)


@patch("chat4me.automation.mouse.pyautogui.click")
def test_click_custom_button(mock_click):
    click(100, 200, button="right", clicks=2)
    mock_click.assert_called_once_with(x=100, y=200, button="right", clicks=2)


@patch("chat4me.automation.mouse.click")
def test_double_click(mock_click):
    double_click(50, 60)
    mock_click.assert_called_once_with(50, 60, clicks=2)


@patch("chat4me.automation.mouse.pyautogui.moveTo")
def test_move_to(mock_move):
    move_to(300, 400, duration=0.5)
    mock_move.assert_called_once_with(300, 400, duration=0.5)


@patch("chat4me.automation.mouse.pyautogui.moveTo")
def test_move_to_default_duration(mock_move):
    move_to(100, 200)
    mock_move.assert_called_once_with(100, 200, duration=0.2)


@patch("chat4me.automation.mouse._pynput_mouse.scroll")
def test_scroll(mock_scroll):
    scroll(3)
    mock_scroll.assert_called_once_with(0, 3)


@patch("chat4me.automation.mouse.pyautogui.position")
def test_get_position(mock_pos):
    mock_pos.return_value = (500, 600)
    pos = get_position()
    assert pos == (500, 600)


@patch("chat4me.automation.mouse.click")
def test_click_center(mock_click):
    click_center(left=10, top=20, width=100, height=50)
    mock_click.assert_called_once_with(60, 45, button="left")
