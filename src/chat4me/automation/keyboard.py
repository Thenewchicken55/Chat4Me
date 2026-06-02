from __future__ import annotations

import pyautogui
from pynput.keyboard import Controller as KeyboardController, Key

_kbd = KeyboardController()


def type_text(text: str, interval: float = 0.05) -> None:
    pyautogui.write(text, interval=interval)


def press_enter() -> None:
    _kbd.tap(Key.enter)


def press_escape() -> None:
    _kbd.tap(Key.esc)


def press_key(key: str) -> None:
    _kbd.tap(key)


def type_and_send(text: str, typing_interval: float = 0.05) -> None:
    type_text(text, interval=typing_interval)
    press_enter()


def hotkey(*keys: str) -> None:
    pyautogui.hotkey(*keys)
