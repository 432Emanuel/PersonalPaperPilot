"""
OCR handler for extracting text from images using pytesseract.
"""

import pytesseract
from PIL import Image
from pathlib import Path

# Configure Tesseract path for Homebrew installation on macOS
pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"


def extract_text_from_image(image_path: str, lang: str = "deu") -> str:
    """
    Extract text from an image file using Tesseract OCR.

    Args:
        image_path: Path to the image file
        lang: Language code for OCR (default: "deu" for German)

    Returns:
        Extracted text as a string
    """
    image = Image.open(image_path)

    # Extract text using pytesseract
    text = pytesseract.image_to_string(image, lang=lang)

    return text.strip()


def extract_text_from_bytes(image_bytes: bytes, lang: str = "deu") -> str:
    """
    Extract text from image bytes using Tesseract OCR.

    Args:
        image_bytes: Image data as bytes
        lang: Language code for OCR (default: "deu" for German)

    Returns:
        Extracted text as a string
    """
    from io import BytesIO

    image = Image.open(BytesIO(image_bytes))
    text = pytesseract.image_to_string(image, lang=lang)

    return text.strip()
