from typing import NamedTuple

import pygetwindow as gw


class WindowInfo(NamedTuple):
    title: str
    left: int
    top: int
    width: int
    height: int


def find_window(substring: str) -> WindowInfo | None:
    matches = [w for w in gw.getWindowsWithTitle(substring) if w.visible and w.width > 0]
    if not matches:
        return None
    w = matches[0]
    return WindowInfo(title=w.title, left=w.left, top=w.top, width=w.width, height=w.height)


def list_windows() -> list[str]:
    return list({w.title for w in gw.getAllWindows() if w.title.strip()})
