# -*- coding: utf-8 -*-
import logging
import traceback
from pathlib import Path
from core.config import LOG_FILE

def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8"
    )

def load_ocr_libraries():
    global convert_from_path, Image, ImageFilter, pytesseract
    from pdf2image import convert_from_path
    from PIL import Image, ImageFilter
    import pytesseract

    from core.config import TESSERACT_CMD
    if TESSERACT_CMD:
        pytesseract.pytesseract.tesseract_cmd = str(TESSERACT_CMD)