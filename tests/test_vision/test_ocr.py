from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

from chat4me.vision.ocr import is_tesseract_available, ocr_image, ocr_image_to_data


@patch("chat4me.vision.ocr.pytesseract.image_to_string")
def test_ocr_image(mock_img_to_str):
    mock_img_to_str.return_value = "Hello World\n"
    img = Image.new("RGB", (100, 50))
    result = ocr_image(img, lang="eng")
    assert result == "Hello World"
    mock_img_to_str.assert_called_once_with(img, lang="eng")


@patch("chat4me.vision.ocr.pytesseract.image_to_string")
def test_ocr_image_with_custom_tesseract(mock_img_to_str):
    mock_img_to_str.return_value = "test"
    img = Image.new("RGB", (10, 10))
    result = ocr_image(img, tesseract_cmd="/custom/tesseract")
    assert result == "test"


@patch("chat4me.vision.ocr.pytesseract.image_to_data")
def test_ocr_image_to_data(mock_img_to_data):
    mock_img_to_data.return_value = {
        "text": ["", "Hello", "", "World", ""],
        "conf": ["-1", "95", "-1", "87", "-1"],
        "left": [0, 10, 0, 50, 0],
        "top": [0, 5, 0, 20, 0],
        "width": [0, 60, 0, 40, 0],
        "height": [0, 15, 0, 15, 0],
    }
    img = Image.new("RGB", (200, 100))
    results = ocr_image_to_data(img, lang="eng")
    assert len(results) == 2
    assert results[0]["text"] == "Hello"
    assert results[0]["conf"] == 95
    assert results[0]["left"] == 10
    assert results[1]["text"] == "World"
    assert results[1]["conf"] == 87


@patch("chat4me.vision.ocr.subprocess.run")
def test_is_tesseract_available_true(mock_run):
    mock_run.return_value = MagicMock()
    assert is_tesseract_available() is True


@patch("chat4me.vision.ocr.subprocess.run")
def test_is_tesseract_available_false(mock_run):
    mock_run.side_effect = FileNotFoundError
    assert is_tesseract_available() is False
