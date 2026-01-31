# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    # إذا كان التطبيق محزماً بـ PyInstaller
    BASE_DIR = Path(sys._MEIPASS)
else:
    # وضع التطوير
    BASE_DIR = Path(__file__).parent.parent

VERSION = "2.0.0"
LOG_FILE = BASE_DIR / "app.log"

def find_existing_path(candidates):
    for p in candidates:
        if p and Path(p).exists():
            return Path(p)
    return None

POPPLER_PATH = find_existing_path([BASE_DIR / 'poppler' / 'bin', os.environ.get('POPPLER_PATH', "")])
TESSERACT_CMD = find_existing_path([BASE_DIR / 'tesseract' / 'tesseract.exe', os.environ.get('TESSERACT_CMD', "")])