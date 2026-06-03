from __future__ import annotations

import pyautogui
from pynput.mouse import Controller as MouseController

_pynput_mouse = MouseController()


def click(x: int, y: int, button: str = "left", clicks: int = 1) -> None:
    """Click at screen coordinates with the specified button and click count."""
    pyautogui.click(x=x, y=y, button=button, clicks=clicks)


def double_click(x: int, y: int) -> None:
    """Double-click at screen coordinates."""
    click(x, y, clicks=2)


def move_to(x: int, y: int, duration: float = 0.2) -> None:
    """Move the mouse to screen coordinates over a duration."""
    pyautogui.moveTo(x, y, duration=duration)


def scroll(clicks: int) -> None:
    """Scroll the mouse wheel by the given number of clicks (positive = up)."""
    _pynput_mouse.scroll(0, clicks)


def get_position() -> tuple[int, int]:
    """Return the current mouse cursor position as (x, y)."""
    x, y = pyautogui.position()
    return int(x), int(y)


def click_center(left: int, top: int, width: int, height: int, button: str = "left") -> None:
    """Click the centre of a rectangle defined by (left, top, width, height)."""
    x = left + width // 2
    y = top + height // 2
    click(x, y, button=button)
