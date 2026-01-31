# -*- coding: utf-8 -*-
"""
ملف تكوين الألوان والثيمات للبرنامج
يحتوي على جميع الألوان والتدرجات المستخدمة في التطبيق
"""

# ============================================
# الألوان الأساسية - الوضع النهاري
# ============================================
LIGHT_COLORS = {
    # الألوان الأساسية
    "primary": "#667eea",
    "primary_dark": "#5568d3",
    "secondary": "#764ba2",
    "accent": "#f093fb",
    
    # ألوان الخلفية
    "background": "#f5f7fa",
    "background_alt": "#e8ecf1",
    "surface": "#ffffff",
    "surface_alt": "#f8f9fa",
    
    # ألوان النصوص
    "text_primary": "#2c3e50",
    "text_secondary": "#6c757d",
    "text_disabled": "#adb5bd",
    
    # ألوان الحدود
    "border": "#e1e8ed",
    "border_focus": "#667eea",
    
    # ألوان الحالة
    "success": "#10b981",
    "success_dark": "#059669",
    "warning": "#f59e0b",
    "warning_dark": "#d97706",
    "error": "#ef4444",
    "error_dark": "#dc2626",
    "info": "#3b82f6",
    "info_dark": "#2563eb",
}

# ============================================
# الألوان الأساسية - الوضع الليلي
# ============================================
DARK_COLORS = {
    # الألوان الأساسية
    "primary": "#4c6ef5",
    "primary_dark": "#3b5bdb",
    "secondary": "#7c3aed",
    "accent": "#ec4899",
    
    # ألوان الخلفية
    "background": "#1a1a2e",
    "background_alt": "#16213e",
    "surface": "#252a3d",
    "surface_alt": "#1e2433",
    
    # ألوان النصوص
    "text_primary": "#e4e4e7",
    "text_secondary": "#9ca3af",
    "text_disabled": "#4b5563",
    
    # ألوان الحدود
    "border": "#374151",
    "border_focus": "#4c6ef5",
    
    # ألوان الحالة
    "success": "#10b981",
    "success_dark": "#059669",
    "warning": "#f59e0b",
    "warning_dark": "#d97706",
    "error": "#ef4444",
    "error_dark": "#dc2626",
    "info": "#3b82f6",
    "info_dark": "#2563eb",
}

# ============================================
# التدرجات اللونية
# ============================================
GRADIENTS = {
    "primary": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:1 #764ba2)",
    "primary_vertical": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #667eea, stop:1 #764ba2)",
    "success": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669)",
    "error": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ef4444, stop:1 #dc2626)",
    "warning": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f59e0b, stop:1 #d97706)",
    "info": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3b82f6, stop:1 #2563eb)",
    "rainbow": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb)",
}

# ============================================
# الأيقونات الإيموجي
# ============================================
ICONS = {
    # أيقونات الأدوات
    "ocr": "🔍",
    "pdf": "📄",
    "security": "🔒",
    "merge": "🔗",
    "split": "✂️",
    "lock": "🔒",
    "unlock": "🔓",
    
    # أيقونات الإجراءات
    "add": "➕",
    "remove": "➖",
    "save": "💾",
    "copy": "📋",
    "paste": "📌",
    "delete": "🗑️",
    "edit": "✏️",
    "search": "🔎",
    "refresh": "🔄",
    "settings": "⚙️",
    
    # أيقونات الحالة
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "loading": "⏳",
    "done": "✓",
    
    # أيقونات الملفات
    "file": "📄",
    "folder": "📁",
    "image": "🖼️",
    "document": "📃",
    
    # أيقونات أخرى
    "home": "🏠",
    "help": "❓",
    "about": "ℹ️",
    "theme_light": "☀️",
    "theme_dark": "🌙",
    "star": "⭐",
    "rocket": "🚀",
    "lightning": "⚡",
    "sparkles": "✨",
}

# ============================================
# إعدادات الخطوط
# ============================================
FONTS = {
    "primary": "Segoe UI",
    "secondary": "Arial",
    "monospace": "Consolas",
    "emoji": "Segoe UI Emoji",
    
    # أحجام الخطوط
    "size_small": 11,
    "size_normal": 13,
    "size_medium": 14,
    "size_large": 16,
    "size_xlarge": 18,
    "size_title": 20,
}

# ============================================
# إعدادات الظلال
# ============================================
SHADOWS = {
    "small": {"blur": 10, "offset": (0, 2), "opacity": 40},
    "medium": {"blur": 20, "offset": (0, 5), "opacity": 60},
    "large": {"blur": 30, "offset": (0, 8), "opacity": 80},
    "xlarge": {"blur": 40, "offset": (0, 10), "opacity": 100},
}

# ============================================
# إعدادات الحواف المستديرة
# ============================================
BORDER_RADIUS = {
    "small": 5,
    "medium": 8,
    "large": 12,
    "xlarge": 16,
    "round": 20,
}

# ============================================
# إعدادات الأنيميشن
# ============================================
ANIMATION = {
    "duration_fast": 150,
    "duration_normal": 300,
    "duration_slow": 600,
    "easing": "OutCubic",
}

# ============================================
# دالة مساعدة للحصول على اللون
# ============================================
def get_color(color_name, is_dark_mode=False):
    """
    الحصول على لون بناءً على الوضع الحالي
    
    Args:
        color_name: اسم اللون
        is_dark_mode: هل الوضع الليلي مفعّل
    
    Returns:
        قيمة اللون
    """
    colors = DARK_COLORS if is_dark_mode else LIGHT_COLORS
    return colors.get(color_name, "#000000")

def get_gradient(gradient_name):
    """
    الحصول على تدرج لوني
    
    Args:
        gradient_name: اسم التدرج
    
    Returns:
        كود التدرج اللوني
    """
    return GRADIENTS.get(gradient_name, GRADIENTS["primary"])

def get_icon(icon_name):
    """
    الحصول على أيقونة
    
    Args:
        icon_name: اسم الأيقونة
    
    Returns:
        رمز الإيموجي
    """
    return ICONS.get(icon_name, "")
