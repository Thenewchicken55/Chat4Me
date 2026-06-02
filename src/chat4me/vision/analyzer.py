from __future__ import annotations

from dataclasses import dataclass, field

from PIL import Image


@dataclass
class TextBlock:
    text: str
    left: int
    top: int
    width: int
    height: int
    confidence: int


@dataclass
class ScreenState:
    text_blocks: list[TextBlock] = field(default_factory=list)
    raw_text: str = ""

    @property
    def has_content(self) -> bool:
        return len(self.text_blocks) > 0

    @property
    def all_text(self) -> str:
        return self.raw_text


def analyze(image: Image.Image, ocr_data: list[dict]) -> ScreenState:
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
    return [b for b in state.text_blocks if text_substring.lower() in b.text.lower()]
