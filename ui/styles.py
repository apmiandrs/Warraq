# -*- coding: utf-8 -*-

# ============================================
# تصميم احترافي متطور مع تدرجات لونية وظلال
# ============================================

LIGHT_STYLESHEET = """
    /* ========== الخلفية العامة ========== */
    QMainWindow, QWidget {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 #f5f7fa, stop:1 #e8ecf1);
        color: #2c3e50;
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }
    
    QLabel {
        background: transparent;
        color: #2c3e50;
    }
    
    /* ========== صناديق المجموعات ========== */
    QGroupBox {
        font-weight: bold;
        font-size: 13px;
        border: 2px solid #e1e8ed;
        border-radius: 10px;
        margin-top: 20px;
        padding: 20px 10px 10px 10px;
        background-color: #ffffff;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top right;
        right: 12px;
        padding: 3px 10px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #667eea, stop:1 #764ba2);
        color: white;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
    }
    
    /* ========== الأزرار ========== */
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 #ffffff, stop:1 #f0f2f5);
        border: 1px solid #e1e8ed;
        padding: 6px 15px;
        border-radius: 6px;
        color: #2c3e50;
        font-size: 12px;
        font-weight: 600;
        min-height: 28px;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #667eea, stop:1 #764ba2);
        border: 2px solid #667eea;
        color: white;
    }
    
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #5568d3, stop:1 #6a3f8f);
        padding-top: 12px;
        padding-bottom: 8px;
    }
    
    QPushButton:disabled {
        background: #e9ecef;
        border: 2px solid #dee2e6;
        color: #adb5bd;
    }
    
    /* ========== حقول الإدخال ========== */
    QTextEdit, QLineEdit {
        background-color: #ffffff;
        border: 2px solid #e1e8ed;
        padding: 8px 12px;
        border-radius: 8px;
        color: #2c3e50;
        font-size: 13px;
        selection-background-color: #667eea;
        selection-color: white;
    }
    
    QTextEdit:focus, QLineEdit:focus {
        border: 2px solid #667eea;
        background-color: #f8f9ff;
    }
    
    /* ========== القوائم المنسدلة ========== */
    QComboBox {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 #ffffff, stop:1 #f8f9fa);
        border: 2px solid #e1e8ed;
        padding: 8px 12px;
        border-radius: 8px;
        color: #2c3e50;
        font-size: 13px;
        min-height: 30px;
    }
    
    QComboBox:hover {
        border: 2px solid #667eea;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 30px;
    }
    
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid #667eea;
        margin-right: 10px;
    }
    
    QComboBox QAbstractItemView {
        background-color: white;
        border: 2px solid #667eea;
        border-radius: 8px;
        selection-background-color: #667eea;
        selection-color: white;
        padding: 5px;
    }
    
    /* ========== شريط التقدم ========== */
    QProgressBar {
        border: none;
        border-radius: 12px;
        text-align: center;
        height: 24px;
        background-color: #e9ecef;
        color: white;
        font-weight: bold;
        font-size: 12px;
    }
    
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
        border-radius: 12px;
    }
    
    /* ========== الرأس (Header) ========== */
    #HeaderFrame {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #667eea, stop:1 #764ba2);
        border: none;
        border-bottom: 3px solid rgba(255, 255, 255, 0.3);
    }
    
    #HeaderFrame QLabel {
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    
    #HeaderFrame QPushButton#headerButton {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: white;
        border-radius: 12px;
        padding: 6px;
    }
    
    #HeaderFrame QPushButton#headerButton:hover {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.35);
    }
    
    #HeaderFrame QPushButton#headerButton:pressed {
        background: rgba(255, 255, 255, 0.12);
        padding-top: 8px;
        padding-bottom: 4px;
    }
    
    /* ========== بطاقات الأدوات ========== */
    #ToolCard {
        background-color: #ffffff;
        border: 2px solid #e1e8ed;
        border-radius: 16px;
    }
    
    #ToolCard:hover {
        border: 2px solid #667eea;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                   stop:0 #667eea, stop:1 #764ba2);
    }
    
    #ToolCard QLabel {
        background: transparent;
        color: #2c3e50;
    }
    
    #cardTitle {
        font-size: 18px;
        font-weight: bold;
        color: #2c3e50;
    }
    
    #cardDesc {
        font-size: 13px;
        color: #6c757d;
    }
    
    #ToolCard:hover #cardTitle, #ToolCard:hover #cardDesc, #ToolCard:hover QLabel {
        color: #ffffff;
    }
    
    /* ========== التبويبات ========== */
    QTabWidget::pane {
        border: 2px solid #e1e8ed;
        border-radius: 10px;
        background: white;
        padding: 5px;
    }
    
    QTabBar::tab {
        padding: 12px 25px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 #f8f9fa, stop:1 #e9ecef);
        border: 2px solid #e1e8ed;
        border-bottom: none;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        margin-left: 3px;
        color: #6c757d;
        font-weight: 600;
    }
    
    QTabBar::tab:selected {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #667eea, stop:1 #764ba2);
        color: white;
        border: 2px solid #667eea;
        border-bottom: none;
    }
    
    QTabBar::tab:hover:!selected {
        background: #e9ecef;
        border: 2px solid #667eea;
    }
    
    /* ========== مربعات الاختيار ========== */
    QCheckBox {
        spacing: 8px;
        color: #2c3e50;
        font-size: 13px;
    }
    
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        border: 2px solid #e1e8ed;
        border-radius: 5px;
        background: white;
    }
    
    QCheckBox::indicator:hover {
        border: 2px solid #667eea;
    }
    
    QCheckBox::indicator:checked {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                   stop:0 #667eea, stop:1 #764ba2);
        border: 2px solid #667eea;
    }
    
    /* ========== شريط الحالة ========== */
    QStatusBar {
        background: #f8f9fa;
        color: #6c757d;
        border-top: 1px solid #e1e8ed;
        font-size: 12px;
    }
    
    /* ========== التلميحات ========== */
    QToolTip {
        background-color: #2c3e50;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 12px;
    }
    
    /* ========== شريط التمرير ========== */
    QScrollBar:vertical {
        background: #f8f9fa;
        width: 12px;
        border-radius: 6px;
        margin: 0;
    }
    
    QScrollBar::handle:vertical {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #667eea, stop:1 #764ba2);
        border-radius: 6px;
        min-height: 30px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #667eea;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }

    /* ========== منطقة السحب والإفلات ========== */
    #dropZone {
        background-color: #f0f7ff;
        border: 2px dashed #667eea;
        border-radius: 12px;
        min-height: 160px;
    }
    
    #dropZone #dropZoneText {
        color: #4a5568;
        font-size: 15px;
        font-weight: 500;
        background: transparent;
    }
    
    #dropZone:hover {
        background-color: #ebf4ff;
        border-color: #764ba2;
    }

    #dropZoneText {
        color: #4a5568 !important;
    }

    /* ========== شريط الحالة الكبسولة ========== */
    #statusCapsule {
        background: rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 15px;
        padding: 2px 12px;
        margin-bottom: 5px;
        margin-right: 15px;
    }
    
    QLabel#statusText {
        color: #2d3436;
        font-size: 12px;
        font-weight: 500;
    }
    
    QLabel#statusIndicator {
        background-color: #00b894;
        border-radius: 4px;
        min-width: 8px;
        min-height: 8px;
        max-width: 8px;
        max-height: 8px;
    }
"""

DARK_STYLESHEET = """
    /* ========== الخلفية العامة - الوضع الليلي ========== */
    QMainWindow, QWidget {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 #1a1a2e, stop:1 #16213e);
        color: #e4e4e7;
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }
    
    QLabel {
        background: transparent;
    }
    
    /* ========== صناديق المجموعات ========== */
    QGroupBox {
        font-weight: bold;
        font-size: 15px;
        border: 2px solid #374151;
        border-radius: 12px;
        margin-top: 25px;
        padding: 30px 15px 15px 15px;
        background-color: #252a3d;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top right;
        right: 15px;
        padding: 5px 15px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #4c6ef5, stop:1 #7c3aed);
        color: white;
        border-radius: 8px;
        font-size: 13px;
        font-weight: bold;
    }
    
    /* ========== الأزرار ========== */
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 #2d3748, stop:1 #1a202c);
        border: 2px solid #374151;
        padding: 10px 20px;
        border-radius: 8px;
        color: #e4e4e7;
        font-size: 13px;
        font-weight: 600;
        min-height: 35px;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #4c6ef5, stop:1 #7c3aed);
        border: 2px solid #4c6ef5;
        color: white;
    }
    
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #3b5bdb, stop:1 #6d28d9);
        padding-top: 12px;
        padding-bottom: 8px;
    }
    
    QPushButton:disabled {
        background: #1e2433;
        border: 2px solid #2d3748;
        color: #4b5563;
    }
    
    /* ========== حقول الإدخال ========== */
    QTextEdit, QLineEdit {
        background-color: #1e2433;
        border: 2px solid #374151;
        padding: 8px 12px;
        border-radius: 8px;
        color: #e4e4e7;
        font-size: 13px;
        selection-background-color: #4c6ef5;
        selection-color: white;
    }
    
    QTextEdit:focus, QLineEdit:focus {
        border: 2px solid #4c6ef5;
        background-color: #252a3d;
    }
    
    /* ========== القوائم المنسدلة ========== */
    QComboBox {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 #2d3748, stop:1 #1e2433);
        border: 2px solid #374151;
        padding: 8px 12px;
        border-radius: 8px;
        color: #e4e4e7;
        font-size: 13px;
        min-height: 30px;
    }
    
    QComboBox:hover {
        border: 2px solid #4c6ef5;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 30px;
    }
    
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid #4c6ef5;
        margin-right: 10px;
    }
    
    QComboBox QAbstractItemView {
        background-color: #1e2433;
        border: 2px solid #4c6ef5;
        border-radius: 8px;
        selection-background-color: #4c6ef5;
        selection-color: white;
        padding: 5px;
        color: #e4e4e7;
    }
    
    /* ========== شريط التقدم ========== */
    QProgressBar {
        border: none;
        border-radius: 12px;
        text-align: center;
        height: 24px;
        background-color: #1e2433;
        color: white;
        font-weight: bold;
        font-size: 12px;
    }
    
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #4c6ef5, stop:0.5 #7c3aed, stop:1 #ec4899);
        border-radius: 12px;
    }
    
    /* ========== الرأس (Header) ========== */
    #HeaderFrame {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #4c6ef5, stop:1 #7c3aed);
        border: none;
        border-bottom: 3px solid rgba(255, 255, 255, 0.2);
    }
    
    #HeaderFrame QLabel {
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    
    #HeaderFrame QPushButton#headerButton {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: white;
        border-radius: 12px;
        padding: 6px;
    }
    
    #HeaderFrame QPushButton#headerButton:hover {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.25);
    }
    
    #HeaderFrame QPushButton#headerButton:pressed {
        background: rgba(0, 0, 0, 0.15);
        padding-top: 8px;
        padding-bottom: 4px;
    }
    
    /* ========== بطاقات الأدوات ========== */
    #ToolCard {
        background-color: #252a3d;
        border: 2px solid #374151;
        border-radius: 16px;
    }
    
    #ToolCard:hover {
        border: 2px solid #4c6ef5;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                   stop:0 #4c6ef5, stop:1 #7c3aed);
    }
    
    #ToolCard QLabel {
        background: transparent;
    }
    
    #cardTitle {
        font-size: 18px;
        font-weight: bold;
        color: #e4e4e7;
    }
    
    #cardDesc {
        font-size: 13px;
        color: #9ca3af;
    }
    
    #ToolCard:hover #cardTitle, #ToolCard:hover #cardDesc {
        color: #ffffff;
    }
    
    /* ========== التبويبات ========== */
    QTabWidget::pane {
        border: 2px solid #374151;
        border-radius: 10px;
        background: #1e2433;
        padding: 5px;
    }
    
    QTabBar::tab {
        padding: 12px 25px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 #2d3748, stop:1 #1a202c);
        border: 2px solid #374151;
        border-bottom: none;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        margin-left: 3px;
        color: #9ca3af;
        font-weight: 600;
    }
    
    QTabBar::tab:selected {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #4c6ef5, stop:1 #7c3aed);
        color: white;
        border: 2px solid #4c6ef5;
        border-bottom: none;
    }
    
    QTabBar::tab:hover:!selected {
        background: #374151;
        border: 2px solid #4c6ef5;
    }
    
    /* ========== مربعات الاختيار ========== */
    QCheckBox {
        spacing: 8px;
        color: #e4e4e7;
        font-size: 13px;
    }
    
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        border: 2px solid #374151;
        border-radius: 5px;
        background: #1e2433;
    }
    
    QCheckBox::indicator:hover {
        border: 2px solid #4c6ef5;
    }
    
    QCheckBox::indicator:checked {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                   stop:0 #4c6ef5, stop:1 #7c3aed);
        border: 2px solid #4c6ef5;
    }
    
    /* ========== شريط الحالة ========== */
    QStatusBar {
        background: #1e2433;
        color: #9ca3af;
        border-top: 1px solid #374151;
        font-size: 12px;
    }
    
    /* ========== التلميحات ========== */
    QToolTip {
        background-color: #374151;
        color: white;
        border: 1px solid #4c6ef5;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 12px;
    }
    
    /* ========== شريط التمرير ========== */
    QScrollBar:vertical {
        background: #1e2433;
        width: 12px;
        border-radius: 6px;
        margin: 0;
    }
    
    QScrollBar::handle:vertical {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #4c6ef5, stop:1 #7c3aed);
        border-radius: 6px;
        min-height: 30px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #4c6ef5;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }

    /* ========== منطقة السحب والإفلات ========== */
    #dropZone {
        background-color: #1e2433;
        border: 2px dashed #4c6ef5;
        border-radius: 12px;
        min-height: 160px;
    }
    
    #dropZone #dropZoneText {
        color: #e4e4e7;
        font-size: 15px;
        font-weight: 500;
        background: transparent;
    }
    
    #dropZone:hover {
        background-color: #252a3d;
        border-color: #7c3aed;
    }
    
    /* ========== التسميات ========== */
    QLabel {
        color: #e4e4e7;
    }

    /* ========== شريط الحالة الكبسولة ========== */
    #statusCapsule {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 2px 12px;
        margin-bottom: 5px;
        margin-right: 15px;
    }
    
    QLabel#statusText {
        color: #e4e4e7;
        font-size: 12px;
        font-weight: 500;
    }
    
    QLabel#statusIndicator {
        background-color: #00d2d3;
        border-radius: 4px;
        min-width: 8px;
        min-height: 8px;
        max-width: 8px;
        max-height: 8px;
    }
"""
