from __future__ import annotations

import pyautogui
from pynput.mouse import Controller as MouseController

_pynput_mouse = MouseController()


def click(x: int, y: int, button: str = "left", clicks: int = 1) -> None:
    pyautogui.click(x=x, y=y, button=button, clicks=clicks)


def double_click(x: int, y: int) -> None:
    click(x, y, clicks=2)


def move_to(x: int, y: int, duration: float = 0.2) -> None:
    pyautogui.moveTo(x, y, duration=duration)


def scroll(clicks: int) -> None:
    _pynput_mouse.scroll(0, clicks)


def get_position() -> tuple[int, int]:
    x, y = pyautogui.position()
    return int(x), int(y)


def click_center(left: int, top: int, width: int, height: int, button: str = "left") -> None:
    x = left + width // 2
    y = top + height // 2
    click(x, y, button=button)
