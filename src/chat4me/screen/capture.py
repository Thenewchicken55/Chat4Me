from pathlib import Path

import mss
from PIL import Image

from chat4me.screen.window import WindowInfo


def capture_window(window: WindowInfo) -> Image.Image:
    """Capture a screenshot of the given window region and return a PIL Image."""
    region = {"left": window.left, "top": window.top, "width": window.width, "height": window.height}
    with mss.mss() as sct:
        sct_img = sct.grab(region)
    return Image.frombytes("RGB", sct_img.size, sct_img.rgb)


def capture_region(left: int, top: int, width: int, height: int) -> Image.Image:
    """Capture a screenshot of an arbitrary screen region."""
    region = {"left": left, "top": top, "width": width, "height": height}
    with mss.mss() as sct:
        sct_img = sct.grab(region)
    return Image.frombytes("RGB", sct_img.size, sct_img.rgb)


def save_screenshot(image: Image.Image, path: str | Path) -> Path:
    """Save a PIL Image to disk, creating parent directories as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(str(path))
    return path
