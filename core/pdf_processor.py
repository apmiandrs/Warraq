# -*- coding: utf-8 -*-
import os
import logging
from pypdf import PdfReader, PdfWriter
from pathlib import Path
from PIL import Image
from pdf2image import convert_from_path

class PDFProcessor:
    """Class to handle advanced PDF operations like merging, splitting, and security."""
    
    @staticmethod
    def merge_pdfs(file_paths, output_path):
        """Merges multiple PDF files into one."""
        current_file = ""
        try:
            writer = PdfWriter()
            for path in file_paths:
                if not path.strip():
                    continue
                
                current_file = Path(path).name
                # التحقق مما إذا كان الملف مشفراً
                reader = PdfReader(path)
                if reader.is_encrypted:
                    return False, f"الملف '{current_file}' محمي بكلمة مرور. يجب فتح الحماية عنه قبل الدمج."
                
                writer.append(path)
            
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            return True, f"تم دمج الملفات بنجاح في: {output_path}"
        except Exception as e:
            logging.error(f"Error merging PDFs at file '{current_file}': {e}")
            error_msg = str(e)
            if "Stream has ended unexpectedly" in error_msg:
                return False, f"فشل الدمج: الملف '{current_file}' يبدو تالفاً أو غير صالح."
            return False, f"خطأ في الملف '{current_file}': {error_msg}"

    @staticmethod
    def split_pdf(file_path, output_dir, page_range_str):
        """Splits a PDF based on a page range string (e.g., '1-3, 5, 8-10')."""
        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            
            pages = PDFProcessor._parse_page_range(page_range_str, total_pages)
            if not pages:
                return False, "نطاق صفحات غير صالح أو خارج نطاق الملف"
            
            writer = PdfWriter()
            for page_num in pages:
                writer.add_page(reader.pages[page_num])
            
            stem = Path(file_path).stem
            # استخدام اسم ملف أكثر دقة
            range_clean = page_range_str.replace(" ", "").replace(",", "_").replace("-", "to")
            output_filename = f"{stem}_pages_{range_clean}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            # تجنب الكتابة فوق ملف موجود بنفس الاسم
            counter = 1
            while os.path.exists(output_path):
                output_path = os.path.join(output_dir, f"{stem}_pages_{range_clean}_{counter}.pdf")
                counter += 1
            
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            return True, f"تم فصل {len(pages)} صفحات بنجاح.\nالملف: {os.path.basename(output_path)}"
        except Exception as e:
            logging.error(f"Error splitting PDF: {e}")
            return False, f"خطأ أثناء الفصل: {str(e)}"

    @staticmethod
    def split_pdf_to_pages(file_path, output_dir):
        """Splits a PDF into individual files, one per page."""
        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            stem = Path(file_path).stem
            
            for i in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                
                output_filename = f"{stem}_page_{i+1}.pdf"
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, "wb") as output_file:
                    writer.write(output_file)
                    
            return True, f"تم فصل {total_pages} صفحة بنجاح في مجلد: {output_dir}"
        except Exception as e:
            logging.error(f"Error splitting PDF to pages: {e}")
            return False, f"خطأ أثناء فصل الصفحات: {str(e)}"

    @staticmethod
    def encrypt_pdf(file_path, password, output_path):
        """Encrypts a PDF with a password."""
        try:
            reader = PdfReader(file_path)
            writer = PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            writer.encrypt(password)
            
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            return True, f"تم قفل الملف بنجاح وحفظه في: {output_path}"
        except Exception as e:
            logging.error(f"Error encrypting PDF: {e}")
            return False, str(e)

    @staticmethod
    def decrypt_pdf(file_path, password, output_path):
        """Decrypts a password-protected PDF."""
        try:
            reader = PdfReader(file_path)
            if reader.is_encrypted:
                reader.decrypt(password)
            
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            return True, f"تم فتح الملف بنجاح وحفظه في: {output_path}"
        except Exception as e:
            logging.error(f"Error decrypting PDF: {e}")
            return False, "تأكد من صحة كلمة المرور"

    @staticmethod
    def images_to_pdf(image_paths, output_path):
        """Converts multiple images into a single PDF."""
        try:
            images = []
            for path in image_paths:
                img = Image.open(path).convert('RGB')
                images.append(img)
            
            if images:
                images[0].save(output_path, save_all=True, append_images=images[1:])
                return True, f"تم تحويل الصور بنجاح إلى: {output_path}"
            return False, "لم يتم العثور على صور لتحويلها"
        except Exception as e:
            logging.error(f"Error converting images to PDF: {e}")
            return False, str(e)

    @staticmethod
    def pdf_to_images(pdf_path, output_dir, poppler_path=None):
        """Converts PDF pages into images."""
        try:
            images = convert_from_path(pdf_path, poppler_path=poppler_path)
            stem = Path(pdf_path).stem
            for i, image in enumerate(images):
                output_path = os.path.join(output_dir, f"{stem}_page_{i+1}.jpg")
                image.save(output_path, 'JPEG')
            return True, f"تم تحويل {len(images)} صفحة إلى صور بنجاح في: {output_dir}"
        except Exception as e:
            logging.error(f"Error converting PDF to images: {e}")
            return False, str(e)

    @staticmethod
    def compress_pdf(pdf_path, output_path):
        """Compresses a PDF file."""
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            
            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)
            
            with open(output_path, "wb") as f:
                writer.write(f)
            return True, f"تم ضغط الملف بنجاح وحفظه في: {output_path}"
        except Exception as e:
            logging.error(f"Error compressing PDF: {e}")
            return False, str(e)

    @staticmethod
    def compress_images(image_paths, output_dir, quality=70):
        """Compresses multiple images."""
        try:
            for path in image_paths:
                img = Image.open(path)
                stem = Path(path).stem
                ext = Path(path).suffix.lower()
                # Ensure we handle transparency correctly if converting to JPEG
                if ext in ['.png', '.bmp'] and quality < 100:
                    img = img.convert('RGB')
                    output_path = os.path.join(output_dir, f"{stem}_compressed.jpg")
                    img.save(output_path, 'JPEG', quality=quality, optimize=True)
                else:
                    output_path = os.path.join(output_dir, f"{stem}_compressed{ext}")
                    img.save(output_path, quality=quality, optimize=True)
            return True, f"تم ضغط الصور بنجاح في: {output_dir}"
        except Exception as e:
            logging.error(f"Error compressing images: {e}")
            return False, str(e)

    @staticmethod
    def _parse_page_range(range_str, total_pages):
        """Helper to parse range strings into a list of 0-indexed page numbers."""
        pages = set()
        try:
            parts = range_str.replace(" ", "").split(',')
            for part in parts:
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    # Convert to 0-indexed and handle boundaries
                    start = max(1, start) - 1
                    end = min(total_pages, end) - 1
                    for i in range(start, end + 1):
                        pages.add(i)
                else:
                    p = int(part)
                    if 1 <= p <= total_pages:
                        pages.add(p - 1)
            return sorted(list(pages))
        except Exception:
            return None
