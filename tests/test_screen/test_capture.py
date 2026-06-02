from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
from PIL import Image

from chat4me.screen.capture import capture_region, capture_window, save_screenshot
from chat4me.screen.window import WindowInfo


class MockMSSImage:
    def __init__(self, size):
        self.size = size
        self.rgb = b"\xff\x00\x00" * (size[0] * size[1])


@patch("chat4me.screen.capture.mss.mss")
def test_capture_window(mock_mss_cls):
    mock_instance = MagicMock()
    mock_mss_cls.return_value.__enter__.return_value = mock_instance
    mock_instance.grab.return_value = MockMSSImage((100, 50))

    window = WindowInfo(title="Test", left=10, top=20, width=100, height=50)
    img = capture_window(window)
    assert isinstance(img, Image.Image)
    assert img.size == (100, 50)
    mock_instance.grab.assert_called_once_with({"left": 10, "top": 20, "width": 100, "height": 50})


@patch("chat4me.screen.capture.mss.mss")
def test_capture_region(mock_mss_cls):
    mock_instance = MagicMock()
    mock_mss_cls.return_value.__enter__.return_value = mock_instance
    mock_instance.grab.return_value = MockMSSImage((200, 100))

    img = capture_region(left=0, top=0, width=200, height=100)
    assert isinstance(img, Image.Image)
    assert img.size == (200, 100)
    mock_instance.grab.assert_called_once_with({"left": 0, "top": 0, "width": 200, "height": 100})


def test_save_screenshot(tmp_path: Path):
    img = Image.new("RGB", (10, 10), color="red")
    p = tmp_path / "sub" / "test.png"
    result = save_screenshot(img, p)
    assert result == p
    assert p.exists()
    assert p.stat().st_size > 0


def test_save_screenshot_default_dir(tmp_path: Path):
    img = Image.new("RGB", (5, 5), color="blue")
    p = tmp_path / "screenshot.png"
    save_screenshot(img, p)
    assert p.exists()
