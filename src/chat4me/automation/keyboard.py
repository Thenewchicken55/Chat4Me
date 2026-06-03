from __future__ import annotations

import pyautogui
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key

_kbd = KeyboardController()


def type_text(text: str, interval: float = 0.05) -> None:
    """Type a string with a configurable per-character delay."""
    pyautogui.write(text, interval=interval)


def press_enter() -> None:
    """Press and release the Enter key."""
    _kbd.tap(Key.enter)


def press_escape() -> None:
    """Press and release the Escape key."""
    _kbd.tap(Key.esc)


def press_key(key: str) -> None:
    """Press and release an arbitrary key by name."""
    _kbd.tap(key)


def type_and_send(text: str, typing_interval: float = 0.05) -> None:
    """Type text then press Enter to send."""
    type_text(text, interval=typing_interval)
    press_enter()


def hotkey(*keys: str) -> None:
    """Press a combination of keys simultaneously."""
    pyautogui.hotkey(*keys)
