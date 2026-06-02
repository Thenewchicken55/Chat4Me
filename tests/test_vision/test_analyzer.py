from PIL import Image

from chat4me.vision.analyzer import ScreenState, TextBlock, analyze, find_text_in_region


def test_screen_state_defaults():
    state = ScreenState()
    assert state.text_blocks == []
    assert state.raw_text == ""
    assert state.has_content is False
    assert state.all_text == ""


def test_screen_state_with_blocks():
    blocks = [
        TextBlock(text="Hello", left=0, top=0, width=50, height=20, confidence=95),
        TextBlock(text="World", left=60, top=0, width=50, height=20, confidence=87),
    ]
    state = ScreenState(text_blocks=blocks, raw_text="Hello\nWorld")
    assert state.has_content is True
    assert state.all_text == "Hello\nWorld"


def test_analyze_creates_blocks():
    ocr_data = [
        {"text": "Hello", "conf": 95, "left": 10, "top": 5, "width": 60, "height": 15},
        {"text": "World", "conf": 87, "left": 50, "top": 20, "width": 40, "height": 15},
    ]
    img = Image.new("RGB", (200, 100))
    state = analyze(img, ocr_data)
    assert len(state.text_blocks) == 2
    assert state.text_blocks[0].text == "Hello"
    assert state.text_blocks[0].confidence == 95
    assert state.text_blocks[1].text == "World"
    assert state.raw_text == "Hello\nWorld"


def test_analyze_empty_data():
    img = Image.new("RGB", (100, 50))
    state = analyze(img, [])
    assert state.text_blocks == []
    assert state.raw_text == ""


def test_find_text_in_region():
    blocks = [
        TextBlock(text="Hello", left=0, top=0, width=50, height=20, confidence=95),
        TextBlock(text="Hello World", left=0, top=30, width=100, height=20, confidence=90),
        TextBlock(text="Goodbye", left=0, top=60, width=70, height=20, confidence=85),
    ]
    state = ScreenState(text_blocks=blocks, raw_text="Hello\nHello World\nGoodbye")
    found = find_text_in_region(state, "hello")
    assert len(found) == 2
    assert all("hello" in b.text.lower() for b in found)


def test_find_text_in_region_no_match():
    blocks = [TextBlock(text="Foo", left=0, top=0, width=30, height=15, confidence=90)]
    state = ScreenState(text_blocks=blocks, raw_text="Foo")
    found = find_text_in_region(state, "Bar")
    assert found == []
