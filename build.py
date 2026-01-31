# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from pathlib import Path
import datetime
import argparse


def build_app(mode="onedir"):
    """بناء التطبيق باستخدام PyInstaller مع سجل مفصل"""

    BASE_DIR = Path(__file__).parent
    POPPLER_DIR = BASE_DIR / "poppler"
    TESSERACT_DIR = BASE_DIR / "tesseract"
    ICON_FILE = BASE_DIR / "icon.ico"
    LOG_FILE = BASE_DIR / f"build_log_{mode}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    # التحقق من وجود المجلدات
    for folder, name in [(POPPLER_DIR, "poppler"), (TESSERACT_DIR, "tesseract")]:
        if not folder.exists():
            print(f"❌ مجلد {name} غير موجود")
            return False

    if not ICON_FILE.exists():
        print("⚠️ أيقونة التطبيق غير موجودة، سيتم البناء بدون أيقونة")
        icon_option = ""
    else:
        icon_option = f"--icon={ICON_FILE}"

    # إعداد خيار النمط (واحد أو مجلد)
    mode_option = "--onedir" if mode == "onedir" else "--onefile"

    # إعداد ملفات البيانات
    # ملاحظة: في ويندوز نستخدم ; للفصل بين المسارات في --add-data
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=Warraq",
        mode_option,
        "--windowed",
        "--noconfirm",  # مسح المجلد الناتج تلقائياً
        "--clean",      # تنظيف الملفات المؤقتة
        icon_option,
        f"--add-data={POPPLER_DIR};poppler",
        f"--add-data={TESSERACT_DIR};tesseract",
        f"--add-data={BASE_DIR / 'warraq.png'};.",
        f"--add-data={BASE_DIR / 'icon.ico'};.",
        f"--add-data={BASE_DIR / 'core'};core",
        f"--add-data={BASE_DIR / 'ui'};ui",
        "--hidden-import=PySide6",
        "--hidden-import=pytesseract",
        "--hidden-import=pdf2image",
        "--hidden-import=pypdf",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageFilter",
        str(BASE_DIR / "main.py")
    ]

    print(f"🚀 بدء بناء التطبيق بنمط ({mode})...")
    print(f"📄 سيتم حفظ سجل البناء في: {LOG_FILE}")

    try:
        with open(LOG_FILE, "w", encoding="utf-8") as log_file:
            subprocess.run(cmd, check=True, text=True, stdout=log_file, stderr=subprocess.STDOUT)
        
        print(f"✅ تم بناء نسخة ({mode}) بنجاح!")
        if mode == "onedir":
            print(f"📦 المجلد الناتج: {BASE_DIR / 'dist' / 'Warraq'}")
        else:
            print(f"📦 الملف الناتج: {BASE_DIR / 'dist' / 'Warraq.exe'}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل البناء، انظر سجل البناء في {LOG_FILE}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller غير مثبت. قم بتثبيته أولاً: pip install pyinstaller")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool to build Warraq application.")
    parser.add_argument("--mode", choices=["onedir", "onefile"], default="onedir", help="Build mode: onedir (default) or onefile")
    parser.add_argument("--both", action="store_true", help="Build both onedir and onefile versions")
    
    args = parser.parse_args()
    
    if args.both:
        print("🔨 بناء كلتا النسختين...")
        s1 = build_app(mode="onedir")
        s2 = build_app(mode="onefile")
        if s1 and s2:
            print("\n✨ تم الانتهاء من بناء النسختين بنجاح!")
    else:
        build_app(mode=args.mode)
