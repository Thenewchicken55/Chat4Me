import subprocess

import pytesseract
from PIL import Image


def ocr_image(image: Image.Image, lang: str = "eng", tesseract_cmd: str | None = None) -> str:
    """Run Tesseract OCR on an image and return the extracted text."""
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    return pytesseract.image_to_string(image, lang=lang).strip()


def ocr_image_to_data(image: Image.Image, lang: str = "eng", tesseract_cmd: str | None = None) -> list[dict]:
    """Run Tesseract OCR and return per-word data (text, confidence, bounding box).

    Results are filtered to only include words with confidence > 0.
    """
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
    results = []
    for i in range(len(data["text"])):
        text = data["text"][i].strip()
        if text and int(data["conf"][i]) > 0:
            results.append({
                "text": text,
                "conf": int(data["conf"][i]),
                "left": data["left"][i],
                "top": data["top"][i],
                "width": data["width"][i],
                "height": data["height"][i],
            })
    return results


def is_tesseract_available(tesseract_cmd: str | None = None) -> bool:
    """Check whether Tesseract is installed and reachable."""
    cmd = tesseract_cmd or "tesseract"
    try:
        subprocess.run([cmd, "--version"], capture_output=True, timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
