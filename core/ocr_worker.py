# -*- coding: utf-8 -*-
import time
import logging
import traceback
from pathlib import Path

from pdf2image import convert_from_path
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import pytesseract
import re

from PySide6.QtCore import QObject, Signal
from core.utils import load_ocr_libraries
from core.config import POPPLER_PATH
from core.corrector import apply_corrections


class OCRWorker(QObject):
    progress = Signal(dict)
    finished = Signal(dict)
    error = Signal(str)
    log = Signal(str)
    page_started = Signal(str)

    def __init__(self):
        super().__init__()
        self._stop_flag = False

    def stop(self):
        """إيقاف العملية بشكل آمن"""
        self._stop_flag = True
        self.log.emit("تم طلب إيقاف العملية.")

    def run_ocr(self, paths, lang="ara+eng", dpi=300, start_page=1, end_page=None, save_txt=True, preprocess=True):
        """تشغيل عملية OCR على الملفات المحددة"""
        try:
            load_ocr_libraries()
        except ImportError as e:
            self.error.emit(f"خطأ في تحميل المكتبات: {e}")
            return

        start_time = time.time()
        extracted_text = []

        try:
            for path in paths:
                if self._stop_flag:
                    self.log.emit("تم إيقاف العملية قبل البدء بالملف.")
                    return

                path = Path(path)
                if not path.is_file():
                    self.error.emit(f"الملف غير موجود: {path}")
                    continue

                # التحويل إلى صور إذا كان PDF
                pages = []
                if path.suffix.lower() == ".pdf":
                    self.log.emit(f"تحويل PDF إلى صور: {path.name}")
                    kwargs = {"dpi": dpi}
                    if POPPLER_PATH:
                        kwargs["poppler_path"] = str(POPPLER_PATH)
                    if end_page:
                        kwargs.update({"first_page": start_page, "last_page": end_page})
                    elif start_page > 1:
                        kwargs["first_page"] = start_page
                    try:
                        pages = convert_from_path(str(path), **kwargs)
                    except Exception as e:
                        self.error.emit(f"خطأ في تحويل PDF إلى صور: {path.name} - {e}")
                        continue
                else:
                    try:
                        pages = [Image.open(path)]
                    except Exception as e:
                        self.error.emit(f"خطأ في فتح الصورة: {path.name} - {e}")
                        continue

                total_pages = len(pages)
                start_idx = max(1, start_page) - 1
                end_idx = min(total_pages, end_page) if end_page else total_pages

                for idx in range(start_idx, end_idx):
                    if self._stop_flag:
                        self.log.emit("تم إيقاف العملية أثناء المعالجة.")
                        return

                    self.page_started.emit(f"معالجة الصفحة {idx + 1} من {total_pages} - {path.name}")

                    img = self._preprocess_image(pages[idx]) if preprocess else pages[idx]
                    self.log.emit(f"OCR صفحة {idx + 1}/{total_pages} ({path.name})")

                    try:
                        # تحسين إعدادات Tesseract للغة العربية والجداول
                        # --oem 1: استخدام LSTM
                        # --psm 3: تقسيم تلقائي للصفحة
                        custom_config = r'--oem 1 --psm 3 -l ' + lang
                        text = pytesseract.image_to_string(img, config=custom_config)
                        text = self._clean_text(text)
                    except Exception as e:
                        text = ""
                        self.error.emit(f"خطأ OCR في صفحة {idx + 1}: {e}")

                    extracted_text.append(f"\n\n--- {path.name} صفحة {idx + 1} ---\n\n{text}")

                    self.progress.emit({
                        "page": idx + 1,
                        "total": total_pages,
                        "text_preview": extracted_text[-1],
                        "elapsed": round(time.time() - start_time, 2)
                    })

            full_text = "".join(extracted_text).strip()
            out_path = ""

            if save_txt and paths and extracted_text:
                try:
                    out_name = "_".join([Path(p).stem for p in paths]) + "_ocr.txt"
                    out_path = str(Path(paths[0]).parent / out_name)
                    Path(out_path).write_text(full_text, encoding="utf-8")
                except Exception as e:
                    self.error.emit(f"فشل حفظ الملف النصي: {e}")

            self.finished.emit({
                "text_path": out_path,
                "text_preview": full_text,
                "total_pages": len(extracted_text),
                "processing_time": round(time.time() - start_time, 2)
            })

        except Exception as ex:
            self.error.emit(f"خطأ غير متوقع: {ex}")
            logging.error(traceback.format_exc())

    def _preprocess_image(self, img: Image.Image) -> Image.Image:
        """معالجة متقدمة للصورة لتحسين دقة OCR دون مكتبات ثقيلة"""
        try:
            # 1. تكبير الصورة (مهم جداً للخطوط الصغيرة والجداول)
            if img.width < 2500:
                scale = 2500 / img.width
                new_size = (2500, int(img.height * scale))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            # 2. تحويل لرمادي
            img = img.convert('L')
            
            # 3. زيادة التباين التلقائي
            img = ImageOps.autocontrast(img)
            
            # 4. تطبيق Thresholding (ثنائية صريحة)
            # أي بكسل أقل من 140 يصبح أسود، والباقي أبيض
            fn = lambda x : 255 if x > 140 else 0
            img = img.point(fn, mode='1')
            
            # 5. تحويلها مجدداً لنمط L للتعامل مع الفلاتر
            img = img.convert('L')
            
            # 6. تصفية الضجيج النهائي
            img = img.filter(ImageFilter.MedianFilter(size=3))
                
            return img
        except Exception as e:
            self.log.emit(f"فشل المعالجة المسبقة للصورة: {e}")
            return img

    def _clean_text(self, text: str) -> str:
        """تنظيف النص المستخرج من ضجيج OCR وتصحيح الأخطاء اللغوية الشائعة"""
        if not text:
            return ""

        # 1. إزالة الرموز الفردية والضجيج اللاتيني غير المفيد
        text = re.sub(r'\b[a-zA-Z]{1,2}\b', '', text)
        
        # 2. إزالة الخطوط الرأسية والرموز العشوائية في بداية ونهاية الأسطر
        text = re.sub(r'^[|I1l!ـ\-\s]+', '', text, flags=re.MULTILINE)
        text = re.sub(r'[|I1l!ـ\-\s]+$', '', text, flags=re.MULTILINE)
        
        # 3. إزالة كلمات الضجيج المحددة (تم توسيعها بناءً على عينة خطاب الشرطة)
        noise_patterns = [
            r'spyall slo', r'sdolall', r'Yigal', r'spall allo', r'allo', r'x 3',
            r'agauwll', r'dual', r'd4loo', r'ulball', r'Giball', r'GoUl', r'ayLalall', r'dylig',
            r'daébie', r'dhbjw', r'optniill', r'diibalo', r'jlo', r'uall', r'oyndil', r'Gahioy',
            r'dotall', r'dylyill', r'uly', r'diya', r'ailoy', r'dos', r'oSule', r'Aulliall',
            r'Glchayl', r'dalollg', r'cliy', r'Bile', r'Lailly', r'amgoll', r'Inalpbig',
            r'oSialaw', r'joss', r'oUY', r'Lol', r'Uonioll', r'Ulgail', r'oSyll', r'dilhlug',
            r'édu', r'Eby', r'jojo', r'agaw', r'Glob', r'ajjc', r'achbil', r'snail', r'agro', r'aollauc'
        ]
        for pattern in noise_patterns:
            text = re.sub(r'\b' + pattern + r'\b', '', text, flags=re.IGNORECASE)

        # 3.5 تنظيف الرموز العشوائية المتبقية
        text = re.sub(r'[@#\$%\^&\*\(\)\{\}\[\]\|\\<>/_]', ' ', text)

        # 4. تصحيحات لغوية سياقية (بناءً على ملف corrector.py)
        text = apply_corrections(text)
            
        # 5. معالجة الأرقام والتواريخ (تصحيح الأخطاء الشائعة في الأرقام العربية)
        text = re.sub(r'([١٢٣٥٦٧٨٩٠])E', r'\1٤', text)
        text = re.sub(r'E([١٢٣٥٦٧٨٩٠])', r'٤\1', text)
        text = re.sub(r'1EEV', r'١٤٤٧', text)
        
        # 6. تنظيف الفراغات والسطور الزائدة
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
