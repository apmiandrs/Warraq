# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from pathlib import Path
import datetime


def build_app():
    """بناء التطبيق باستخدام PyInstaller مع سجل مفصل"""

    BASE_DIR = Path(__file__).parent
    POPPLER_DIR = BASE_DIR / "poppler"
    TESSERACT_DIR = BASE_DIR / "tesseract"
    ICON_FILE = BASE_DIR / "icon.ico"
    LOG_FILE = BASE_DIR / f"build_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

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

    # إعداد ملفات البيانات
    # ملاحظة: في ويندوز نستخدم ; للفصل بين المسارات في --add-data
    cmd = [
        "pyinstaller",
        "--name=PDF_Image_to_Text_Converter",
        "--onedir",
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
        "--hidden-import=pytesseract",
        "--hidden-import=pdf2image",
        "--hidden-import=pypdf",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageFilter",
        str(BASE_DIR / "main.py")
    ]

    print("🚀 بدء بناء التطبيق...")
    print(f"📄 سيتم حفظ سجل البناء في: {LOG_FILE}")

    try:
        with open(LOG_FILE, "w", encoding="utf-8") as log_file:
            subprocess.run(cmd, check=True, text=True, stdout=log_file, stderr=subprocess.STDOUT)
        
        print("✅ تم بناء التطبيق بنجاح!")
        print(f"📦 المجلد الناتج: {BASE_DIR / 'dist' / 'PDF_Image_to_Text_Converter'}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل البناء، انظر سجل البناء في {LOG_FILE}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller غير مثبت. قم بتثبيته أولاً: pip install pyinstaller")
        return False


def self_copy_files(dist_dir, base_dir):
    """نسخ الملفات الإضافية إلى مجلد التوزيع"""
    import shutil

    # إنشاء المجلدات إذا لم تكن موجودة
    (dist_dir / "core").mkdir(exist_ok=True)
    (dist_dir / "ui").mkdir(exist_ok=True)

    # نسخ ملفات core
    core_files = ["config.py", "utils.py", "ocr_worker.py", "__init__.py"]
    for file in core_files:
        src = base_dir / "core" / file
        if src.exists():
            shutil.copy2(src, dist_dir / "core" / file)

    # نسخ ملفات ui
    ui_files = ["main_window.py", "custom_widgets.py", "styles.py", "__init__.py"]
    for file in ui_files:
        src = base_dir / "ui" / file
        if src.exists():
            shutil.copy2(src, dist_dir / "ui" / file)

    print("📋 تم نسخ الملفات الإضافية إلى مجلد التوزيع")


if __name__ == "__main__":
    build_app()