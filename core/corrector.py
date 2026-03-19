# -*- coding: utf-8 -*-

# تصحيحات لغوية سياقية (بناءً على العينة والجدول المحدث)
OCR_CORRECTIONS = {
    # --- رموز أجنبية وضجيج (حذف نهائي) ---
    "ayli": "",
    "abl": "",
    "yall": "",
    "ow": "",
    "]": "",
    "أو !": "",
    "!": ""
}

def apply_corrections(text):
    """تطبيق التصحيحات اللغوية على النص"""
    if not text:
        return ""
    
    for wrong, right in OCR_CORRECTIONS.items():
        text = text.replace(wrong, right)
    
    return text
