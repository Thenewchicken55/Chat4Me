from __future__ import annotations

from dataclasses import dataclass, field

from PIL import Image


@dataclass
class TextBlock:
    """A single OCR-detected word with its position, size, and confidence."""

    text: str
    left: int
    top: int
    width: int
    height: int
    confidence: int


@dataclass
class ScreenState:
    """The full screen state extracted from a screenshot: OCR blocks and raw text."""

    text_blocks: list[TextBlock] = field(default_factory=list)
    raw_text: str = ""

    @property
    def has_content(self) -> bool:
        """Return True when at least one text block was detected."""
        return len(self.text_blocks) > 0

    @property
    def all_text(self) -> str:
        """Return the concatenated raw text of all detected blocks."""
        return self.raw_text


def filter_message_area(blocks: list[TextBlock], window_width: int) -> list[TextBlock]:
    """Keep only text blocks from the main chat area, excluding the sidebar and top bar."""
    sidebar_width = max(240, int(window_width * 0.15))
    return [b for b in blocks if b.left >= sidebar_width and b.top > 50]


def analyze(image: Image.Image, ocr_data: list[dict]) -> ScreenState:
    """Convert raw OCR data into a ScreenState of TextBlocks and raw text."""
    blocks = []
    for item in ocr_data:
        blocks.append(
            TextBlock(
                text=item["text"],
                left=item["left"],
                top=item["top"],
                width=item["width"],
                height=item["height"],
                confidence=item["conf"],
            )
        )
    raw = "\n".join(b.text for b in blocks)
    return ScreenState(text_blocks=blocks, raw_text=raw)


def find_text_in_region(state: ScreenState, text_substring: str) -> list[TextBlock]:
    """Find all text blocks whose text contains the given substring (case-insensitive)."""
    return [b for b in state.text_blocks if text_substring.lower() in b.text.lower()]


def find_channels(state: ScreenState, window_width: int) -> list[TextBlock]:
    """Find text blocks in the left sidebar region likely to be Discord channel names."""
    sidebar_width = max(240, int(window_width * 0.15))
    return [b for b in state.text_blocks if b.left < sidebar_width and b.confidence > 50]
