# -*- coding: utf-8 -*-
import time
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QLabel, QComboBox, QCheckBox,
    QLineEdit, QGroupBox, QScrollArea, QTextEdit, QProgressBar,
    QStackedWidget, QTabWidget, QFrame, QMessageBox, QGraphicsOpacityEffect,
    QSizePolicy, QStatusBar
)
from PySide6.QtCore import Qt, QThread, Signal, QPropertyAnimation, QEasingCurve, QSize, QParallelAnimationGroup, QSequentialAnimationGroup, QTimer
from PySide6.QtGui import QFont, QDragEnterEvent, QDropEvent, QIntValidator, QIcon, QPixmap

from core.ocr_worker import OCRWorker
from core.pdf_processor import PDFProcessor
from core.config import VERSION
from ui.styles import LIGHT_STYLESHEET, DARK_STYLESHEET
from ui.custom_widgets import NotificationPopup, ProgressDialog, CreditsDialog
from ui.icon_factory import IconFactory


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_files = []
        self.ocr_thread = None
        self.ocr_worker = None
        self.is_dark_mode = False
        self.progress_dialog = None
        
        # دعم اللغة العربية (يمين إلى يسار)
        self.setLayoutDirection(Qt.RightToLeft)
        
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(f"المساعد الذكي للملفات - الإصدار {VERSION}")
        self.setMinimumSize(1000, 750)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Header (Common)
        self.create_header()
        
        # Stacked Widget for different pages
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # شريط الحالة السفلي (تصميم كبسولة)
        self.status_bar = QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        self.status_bar.setFixedHeight(35)
        self.setStatusBar(self.status_bar)
        
        self.status_capsule = QFrame()
        self.status_capsule.setObjectName("statusCapsule")
        capsule_layout = QHBoxLayout(self.status_capsule)
        capsule_layout.setContentsMargins(10, 0, 10, 0)
        capsule_layout.setSpacing(8)
        
        self.status_indicator = QLabel()
        self.status_indicator.setObjectName("statusIndicator")
        capsule_layout.addWidget(self.status_indicator)
        
        self.current_status_label = QLabel("جاهز")
        self.current_status_label.setObjectName("statusText")
        capsule_layout.addWidget(self.current_status_label)
        
        self.status_bar.addPermanentWidget(self.status_capsule)
        
        # Create Pages
        self.page_dashboard = QWidget()
        self.page_ocr = QWidget()
        self.page_pdf_tools = QWidget()
        self.page_security = QWidget()
        
        self.stacked_widget.addWidget(self.page_dashboard)
        self.stacked_widget.addWidget(self.page_ocr)
        self.stacked_widget.addWidget(self.page_pdf_tools)
        self.stacked_widget.addWidget(self.page_security)
        
        # Setup Page Layouts
        self.setup_dashboard_page()
        self.setup_ocr_page()
        self.setup_pdf_tools_page()
        self.setup_security_page()
        
        # Apply Default Theme
        self.apply_light_theme()
        
        # Start at Dashboard
        self.stacked_widget.setCurrentIndex(0)

    def create_header(self):
        header_frame = QFrame()
        header_frame.setObjectName("HeaderFrame")
        header_frame.setFixedHeight(70)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(25, 10, 25, 10)
        header_layout.setSpacing(15)
        
        # صندوق العنوان (تصميم عصري يشبه البحث)
        self.title_container = QFrame()
        self.title_container.setObjectName("titleContainer")
        self.title_container.setStyleSheet("""
            QFrame#titleContainer {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 2px 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)
        title_layout = QHBoxLayout(self.title_container)
        title_layout.setContentsMargins(10, 0, 10, 0)
        
        self.title_label = QLabel("المساعد الذكي للملفات")
        self.title_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.title_label.setStyleSheet("color: white; background: transparent;")
        
        self.title_icon = QLabel()
        logo_pixmap = QPixmap(str(Path(__file__).parent.parent / "warraq.png"))
        self.title_icon.setPixmap(logo_pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.title_icon.setStyleSheet("background: transparent;")
        
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.title_icon)
        
        header_layout.addWidget(self.title_container)
        
        header_layout.addStretch()
        
        # زر الرئيسية
        self.nav_home_btn = QPushButton()
        self.nav_home_btn.setIcon(IconFactory.create_icon("home", size=40))
        self.nav_home_btn.setIconSize(QSize(28, 28))
        self.nav_home_btn.setObjectName("headerButton")
        self.nav_home_btn.setFixedSize(54, 48)
        self.nav_home_btn.setToolTip("الرئيسية")
        self.nav_home_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        header_layout.addWidget(self.nav_home_btn)
        
        # زر الثيم
        self.theme_btn = QPushButton()
        self.theme_btn.setIcon(IconFactory.create_icon("moon", size=40))
        self.theme_btn.setIconSize(QSize(28, 28))
        self.theme_btn.setObjectName("headerButton")
        self.theme_btn.setFixedSize(54, 48)
        self.theme_btn.setToolTip("تبديل الوضع")
        self.theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_btn)
        
        # زر المعلومات
        self.credits_btn = QPushButton()
        self.credits_btn.setIcon(IconFactory.create_icon("info", size=40))
        self.credits_btn.setIconSize(QSize(28, 28))
        self.credits_btn.setObjectName("headerButton")
        self.credits_btn.setFixedSize(54, 48)
        self.credits_btn.setToolTip("حول البرنامج")
        self.credits_btn.clicked.connect(self.show_credits)
        header_layout.addWidget(self.credits_btn)
        
        self.main_layout.addWidget(header_frame)

    def setup_dashboard_page(self):
        layout = QVBoxLayout(self.page_dashboard)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # إضافة الشعار الكبير في الداشبورد
        logo_label = QLabel()
        logo_pixmap = QPixmap(str(Path(__file__).parent.parent / "warraq.png"))
        logo_label.setPixmap(logo_pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        welcome_label = QLabel("مرحباً بك في المساعد الذكي للملفات")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(welcome_label)
        
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        self.ocr_card = self.create_tool_card("search", "استخراج النصوص", "تحويل الصور و PDF إلى نص عربي دقيق", 1)
        self.pdf_card = self.create_tool_card("file", "أدوات الصفحات", "دمج وفصل ملفات PDF بسهولة", 2)
        self.security_card = self.create_tool_card("lock", "أمان الملفات", "قفل وحماية الملفات بكلمة مرور", 3)
        
        cards_layout.addWidget(self.ocr_card)
        cards_layout.addWidget(self.pdf_card)
        cards_layout.addWidget(self.security_card)
        
        layout.addLayout(cards_layout)
        layout.addStretch()
        
        footer = QLabel("تصميم وتطوير م/ عبدالله الغميز")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        layout.addWidget(footer)

    def create_tool_card(self, icon, title, desc, index):
        card = QFrame()
        card.setObjectName("ToolCard")
        card.setFixedSize(280, 220)
        card.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # أيقونة موحدة الحجم
        icon_label = QLabel()
        icon_label.setObjectName("cardIconLabel") # Add object name to target in style
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedHeight(80)
        icon_label.setPixmap(IconFactory.create_icon(icon, color="#2c3e50", size=80).pixmap(64, 64))
        layout.addWidget(icon_label)
        
        # العنوان
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # الوصف
        desc_label = QLabel(desc)
        desc_label.setObjectName("cardDesc")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # إضافة تأثير الظل
        card.setGraphicsEffect(self.create_shadow_effect())
        
        # حفظ المراجع للتسميات
        card._icon_label = icon_label
        card._title_label = title_label
        card._desc_label = desc_label
        
        # ضبط اللون الأولي بناءً على الثيم الحالي
        is_dark = self.is_dark_mode
        init_color = "white" if is_dark else "#2c3e50"
        init_desc_color = "rgba(255, 255, 255, 0.9)" if is_dark else "#6c757d"
        title_label.setStyleSheet(f"color: {init_color}; background: transparent; font-size: 18px; font-weight: bold;")
        desc_label.setStyleSheet(f"color: {init_desc_color}; background: transparent; font-size: 13px;")
        
        # تأثير hover لتغيير الألوان
        def on_enter(e):
            icon_label.setPixmap(IconFactory.create_icon(icon, color="white", size=80).pixmap(64, 64))
            title_label.setStyleSheet("color: white; background: transparent; font-size: 18px; font-weight: bold;")
            desc_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: transparent; font-size: 13px;")
            self.animate_card_hover(card, True)
        
        def on_leave(e):
            is_dark = self.is_dark_mode
            color = "white" if is_dark else "#2c3e50"
            desc_color = "rgba(255, 255, 255, 0.9)" if is_dark else "#6c757d"
            
            icon_label.setPixmap(IconFactory.create_icon(icon, color=color, size=80).pixmap(64, 64))
            title_label.setStyleSheet(f"color: {color}; background: transparent; font-size: 18px; font-weight: bold;")
            desc_label.setStyleSheet(f"color: {desc_color}; background: transparent; font-size: 13px;")
            self.animate_card_hover(card, False)
        
        card.enterEvent = on_enter
        card.leaveEvent = on_leave
        
        # إضافة تأثير حركي عند النقر
        def animated_click(e):
            self.animate_card_click(card)
            QTimer.singleShot(200, lambda: self.stacked_widget.setCurrentIndex(index))
        
        card.mousePressEvent = animated_click
        
        return card
    
    def create_shadow_effect(self):
        """إنشاء تأثير ظل للبطاقات"""
        from PySide6.QtWidgets import QGraphicsDropShadowEffect
        from PySide6.QtGui import QColor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 5)
        return shadow
    
    def animate_card_hover(self, card, entering):
        """تأثير حركي عند تمرير الماوس على البطاقة"""
        animation = QPropertyAnimation(card, b"geometry")
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        
        current_geo = card.geometry()
        if entering:
            # رفع البطاقة قليلاً
            new_geo = current_geo.adjusted(-5, -5, 5, 5)
        else:
            # إعادة البطاقة لحجمها الأصلي
            new_geo = current_geo.adjusted(5, 5, -5, -5)
        
        animation.setStartValue(current_geo)
        animation.setEndValue(new_geo)
        animation.start()
        
        # حفظ الأنيميشن لمنع حذفها
        if not hasattr(card, '_animations'):
            card._animations = []
        card._animations.append(animation)
    
    def animate_card_click(self, card):
        """تأثير حركي عند النقر على البطاقة"""
        # تأثير الضغط
        animation = QPropertyAnimation(card, b"geometry")
        animation.setDuration(100)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        current_geo = card.geometry()
        pressed_geo = current_geo.adjusted(3, 3, -3, -3)
        
        animation.setStartValue(current_geo)
        animation.setEndValue(pressed_geo)
        animation.start()
        
        # العودة للحجم الطبيعي
        QTimer.singleShot(100, lambda: self.animate_card_release(card, pressed_geo, current_geo))

    def animate_card_release(self, card, start_geo, end_geo):
        """إعادة البطاقة لحجمها الطبيعي بعد النقر"""
        animation = QPropertyAnimation(card, b"geometry")
        animation.setDuration(100)
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.setStartValue(start_geo)
        animation.setEndValue(end_geo)
        animation.start()
    
    def setup_ocr_page(self):
        # تخطيط الصفحة الرئيسي
        main_layout = QVBoxLayout(self.page_ocr)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # إنشاء منطقة تمرير لتكون الواجهة مرنة
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)
        
        # Drop Zone
        self.create_drop_zone(layout)
        
        # Controls
        self.create_controls(layout)
        
        # Progress
        self.create_progress_section(layout)
        
        # Results
        self.create_results_section(layout)
        
        # إضافة مساحة مرنة في الأسفل
        layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def setup_pdf_tools_page(self):
        layout = QVBoxLayout(self.page_pdf_tools)
        layout.setContentsMargins(30, 20, 30, 20)
        
        tabs = QTabWidget()
        
        # Merge Tab
        merge_tab = QWidget()
        m_layout = QVBoxLayout(merge_tab)
        m_layout.addWidget(QLabel("دمج ملفات PDF:"))
        
        self.merge_list = QTextEdit()
        self.merge_list.setPlaceholderText("قائمة الملفات المراد دمجها...")
        self.merge_list.setReadOnly(True)
        m_layout.addWidget(self.merge_list)
        
        m_btns = QHBoxLayout()
        add_btn = QPushButton("➕ إضافة ملفات")
        add_btn.clicked.connect(self.choose_merge_files)
        clear_btn = QPushButton("🧹 مسح القائمة")
        clear_btn.clicked.connect(lambda: self.merge_list.clear())
        m_btns.addWidget(add_btn)
        m_btns.addWidget(clear_btn)
        m_layout.addLayout(m_btns)
        
        self.exec_merge_btn = QPushButton("🔗 دمج وحفظ الملف")
        self.exec_merge_btn.setStyleSheet("background-color: #2E7D32; color: white;")
        self.exec_merge_btn.clicked.connect(self.run_merge)
        m_layout.addWidget(self.exec_merge_btn)
        
        tabs.addTab(merge_tab, "🔗 دمج")
        
        # Split Tab
        split_tab = QWidget()
        s_layout = QVBoxLayout(split_tab)
        s_layout.addWidget(QLabel("فصل صفحات PDF:"))
        
        s_file_row = QHBoxLayout()
        self.split_file_input = QLineEdit()
        self.split_file_input.setPlaceholderText("اختر ملف PDF...")
        s_browse = QPushButton("📁")
        s_browse.clicked.connect(self.choose_split_file)
        s_file_row.addWidget(self.split_file_input)
        s_file_row.addWidget(s_browse)
        s_layout.addLayout(s_file_row)
        
        s_layout.addWidget(QLabel("نطاق الصفحات (مثال: 1-5, 8, 10-12):"))
        range_row = QHBoxLayout()
        self.split_range_input = QLineEdit()
        range_row.addWidget(self.split_range_input)
        
        self.split_each_page_check = QCheckBox("فصل كل صفحة في ملف مستقل")
        self.split_each_page_check.stateChanged.connect(self.toggle_split_range)
        range_row.addWidget(self.split_each_page_check)
        s_layout.addLayout(range_row)
        
        self.exec_split_btn = QPushButton("✂️ فصل وحفظ")
        self.exec_split_btn.clicked.connect(self.run_split)
        s_layout.addWidget(self.exec_split_btn)
        s_layout.addStretch()
        
        tabs.addTab(split_tab, "✂️ فصل")
        layout.addWidget(tabs)

    def setup_security_page(self):
        layout = QVBoxLayout(self.page_security)
        layout.setContentsMargins(30, 20, 30, 20)
        
        tabs = QTabWidget()
        
        # Lock Tab
        lock_tab = QWidget()
        l_layout = QVBoxLayout(lock_tab)
        l_layout.addWidget(QLabel("قفل ملف PDF بكلمة مرور:"))
        
        l_file_row = QHBoxLayout()
        self.lock_file_input = QLineEdit()
        self.lock_file_input.setPlaceholderText("اختر ملف PDF...")
        l_browse = QPushButton("📁")
        l_browse.clicked.connect(self.choose_lock_file)
        l_file_row.addWidget(self.lock_file_input)
        l_file_row.addWidget(l_browse)
        l_layout.addLayout(l_file_row)
        
        l_layout.addWidget(QLabel("كلمة المرور:"))
        self.lock_pass_input = QLineEdit()
        self.lock_pass_input.setEchoMode(QLineEdit.Password)
        l_layout.addWidget(self.lock_pass_input)
        
        self.exec_lock_btn = QPushButton("🔒 قفل وحفظ")
        self.exec_lock_btn.clicked.connect(self.run_encrypt)
        l_layout.addWidget(self.exec_lock_btn)
        l_layout.addStretch()
        
        tabs.addTab(lock_tab, "🔒 قفل")
        
        # Unlock Tab
        unlock_tab = QWidget()
        u_layout = QVBoxLayout(unlock_tab)
        u_layout.addWidget(QLabel("فتح ملف PDF محمي:"))
        
        u_file_row = QHBoxLayout()
        self.unlock_file_input = QLineEdit()
        self.unlock_file_input.setPlaceholderText("اختر ملف PDF المحمي...")
        u_browse = QPushButton("📁")
        u_browse.clicked.connect(self.choose_unlock_file)
        u_file_row.addWidget(self.unlock_file_input)
        u_file_row.addWidget(u_browse)
        u_layout.addLayout(u_file_row)
        
        u_layout.addWidget(QLabel("كلمة المرور الحالية:"))
        self.unlock_pass_input = QLineEdit()
        self.unlock_pass_input.setEchoMode(QLineEdit.Password)
        u_layout.addWidget(self.unlock_pass_input)
        
        self.exec_unlock_btn = QPushButton("🔓 فتح وحفظ نسخة")
        self.exec_unlock_btn.clicked.connect(self.run_decrypt)
        u_layout.addWidget(self.exec_unlock_btn)
        u_layout.addStretch()
        
        tabs.addTab(unlock_tab, "🔓 فتح")
        layout.addWidget(tabs)

    # --- Re-add OCR missing methods ---
    def create_drop_zone(self, parent_layout):
        drop_group = QGroupBox("اسحب وأسقط الملفات هنا")
        drop_layout = QVBoxLayout(drop_group)
        drop_layout.setContentsMargins(25, 30, 25, 25)
        drop_layout.setSpacing(20)
        
        # منطقة السحب والإفلات (استخدام حاوية لتطبيق الستايل)
        self.drop_container = QFrame()
        self.drop_container.setObjectName("dropZone")
        self.drop_container.setMinimumHeight(180)
        self.drop_container.setAcceptDrops(True)
        self.drop_container.setCursor(Qt.PointingHandCursor)
        self.drop_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        container_layout = QVBoxLayout(self.drop_container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        
        self.drop_label = QLabel()
        self.drop_label.setObjectName("dropZoneText")
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setText("📁\n\nاسحب الملفات هنا\nأو انقر لاختيار ملفات من جهازك\n\n(PDF, PNG, JPG, BMP, TIFF)")
        self.drop_label.setAcceptDrops(False) # التسمية لا تستقبل السحب، المستوعب هو من يفعل
        
        container_layout.addWidget(self.drop_label)
        
        # ربط أحداث السحب للمستوعب
        self.drop_container.dragEnterEvent = self.drag_enter_event
        self.drop_container.dropEvent = self.drop_event
        self.drop_container.mousePressEvent = lambda e: self.choose_files()
        
        drop_layout.addWidget(self.drop_container)
        
        # زر اختيار الملفات كخيار بديل واضح
        self.choose_btn = QPushButton("📂 اختر ملفات من الجهاز")
        self.choose_btn.setMinimumHeight(50)
        self.choose_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.choose_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                font-weight: bold;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #5a6fd6, stop:1 #6a4392);
            }
        """)
        self.choose_btn.clicked.connect(self.choose_files)
        drop_layout.addWidget(self.choose_btn)
        
        # معلومات الملفات المختارة
        self.file_list_label = QLabel("لم يتم اختيار ملفات بعد.")
        self.file_list_label.setStyleSheet("color: #6c757d; font-size: 13px; padding: 10px;")
        self.file_list_label.setWordWrap(True)
        self.file_list_label.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(self.file_list_label)
        
        parent_layout.addWidget(drop_group)

    def create_controls(self, parent_layout):
        from PySide6.QtWidgets import QGridLayout
        
        controls_group = QGroupBox("إعدادات التحويل")
        controls_layout = QGridLayout(controls_group)
        controls_layout.setContentsMargins(25, 30, 25, 25)
        controls_layout.setHorizontalSpacing(30)
        controls_layout.setVerticalSpacing(20)
        
        # الصف الأول: اللغة و DPI
        lang_label = QLabel("اللغة:")
        lang_label.setStyleSheet("font-weight: bold;")
        controls_layout.addWidget(lang_label, 0, 0)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["عربي + إنجليزي", "فقط عربي", "فقط إنجليزي"])
        self.lang_combo.setMinimumWidth(250)
        self.lang_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        controls_layout.addWidget(self.lang_combo, 0, 1)
        
        dpi_label = QLabel("دقة الصورة (DPI):")
        dpi_label.setStyleSheet("font-weight: bold;")
        controls_layout.addWidget(dpi_label, 0, 2)
        
        self.dpi_spin = QLineEdit("300")
        self.dpi_spin.setValidator(QIntValidator(100, 600))
        self.dpi_spin.setMinimumWidth(100)
        self.dpi_spin.setMaximumWidth(150)
        controls_layout.addWidget(self.dpi_spin, 0, 3)
        
        # الصف الثاني: نطاق الصفحات
        pages_label = QLabel("نطاق الصفحات:")
        pages_label.setStyleSheet("font-weight: bold;")
        controls_layout.addWidget(pages_label, 1, 0)
        
        pages_widget = QWidget()
        pages_sub_layout = QHBoxLayout(pages_widget)
        pages_sub_layout.setContentsMargins(0, 0, 0, 0)
        pages_sub_layout.setSpacing(15)
        
        pages_sub_layout.addWidget(QLabel("من:"))
        self.start_page_spin = QLineEdit("1")
        self.start_page_spin.setValidator(QIntValidator(1, 9999))
        self.start_page_spin.setMinimumWidth(70)
        self.start_page_spin.setMaximumWidth(100)
        pages_sub_layout.addWidget(self.start_page_spin)
        
        pages_sub_layout.addWidget(QLabel("إلى:"))
        self.end_page_spin = QLineEdit()
        self.end_page_spin.setValidator(QIntValidator(1, 9999))
        self.end_page_spin.setMinimumWidth(70)
        self.end_page_spin.setMaximumWidth(100)
        self.end_page_spin.setPlaceholderText("الكل")
        pages_sub_layout.addWidget(self.end_page_spin)
        pages_sub_layout.addStretch()
        
        controls_layout.addWidget(pages_widget, 1, 1, 1, 3)
        
        # الصف الثالث: المعالجة المسبقة
        self.preprocess_check = QCheckBox("تفعيل المعالجة المسبقة للصور (يحسن دقة النصوص العربية)")
        self.preprocess_check.setChecked(True)
        self.preprocess_check.setStyleSheet("font-weight: 500; margin-top: 10px;")
        controls_layout.addWidget(self.preprocess_check, 2, 0, 1, 4)
        
        # جعل الأعمدة تتمدد بشكل متساوي
        controls_layout.setColumnStretch(1, 2)
        controls_layout.setColumnStretch(3, 1)
        
        parent_layout.addWidget(controls_group)

    def create_progress_section(self, parent_layout):
        progress_group = QGroupBox("حالة المجلد")
        progress_layout = QVBoxLayout(progress_group)
        progress_layout.setContentsMargins(20, 25, 20, 20)
        progress_layout.setSpacing(12)
        
        self.current_page_label = QLabel("انتظار الملفات...")
        self.current_page_label.setStyleSheet("font-weight: 500;")
        progress_layout.addWidget(self.current_page_label)
        
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)
        
        stats_layout = QHBoxLayout()
        self.page_stats_label = QLabel("0/0")
        self.time_stats_label = QLabel("00:00")
        stats_layout.addWidget(self.page_stats_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.time_stats_label)
        progress_layout.addLayout(stats_layout)
        
        btns = QHBoxLayout()
        btns.setSpacing(15)
        self.start_btn = QPushButton("🚀 بدء OCR")
        self.start_btn.setMinimumHeight(45)
        self.start_btn.clicked.connect(self.start_ocr)
        
        self.stop_btn = QPushButton("🛑 إيقاف")
        self.stop_btn.setMinimumHeight(45)
        self.stop_btn.clicked.connect(self.stop_ocr)
        self.stop_btn.setEnabled(False)
        
        btns.addWidget(self.start_btn, 2) # Start button takes more space
        btns.addWidget(self.stop_btn, 1) # Stop button takes less space
        progress_layout.addLayout(btns)
        
        parent_layout.addWidget(progress_group)

    def create_results_section(self, parent_layout):
        results_group = QGroupBox("النتائج")
        results_layout = QVBoxLayout(results_group)
        results_layout.setContentsMargins(20, 25, 20, 20)
        results_layout.setSpacing(12)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("ستظهر النتائج هنا بعد التحويل...")
        results_layout.addWidget(self.text_edit)
        
        btns = QHBoxLayout()
        btns.setSpacing(10)
        
        copy_btn = QPushButton("📋 نسخ")
        copy_btn.setMinimumWidth(120)
        copy_btn.clicked.connect(self.copy_text)
        
        save_btn = QPushButton("💾 حفظ")
        save_btn.setMinimumWidth(120)
        save_btn.clicked.connect(self.save_text)
        
        self.word_count_label = QLabel("0 كلمات")
        self.char_count_label = QLabel("0 أحرف")
        self.word_count_label.setStyleSheet("color: #6c757d; font-size: 12px;")
        self.char_count_label.setStyleSheet("color: #6c757d; font-size: 12px;")
        
        btns.addWidget(copy_btn)
        btns.addWidget(save_btn)
        btns.addStretch()
        btns.addWidget(self.word_count_label)
        btns.addWidget(self.char_count_label)
        results_layout.addLayout(btns)
        
        parent_layout.addWidget(results_group)
    def toggle_theme(self):
        """تبديل بين الوضع النهاري والليلي مع تأثير انتقالي"""
        # تأثير fade out/in
        self.animate_theme_transition()
        
        if self.is_dark_mode:
            QTimer.singleShot(150, self.apply_light_theme)
            self.theme_btn.setIcon(IconFactory.create_icon("moon", size=40))
            self.update_card_icons(is_dark=False)
        else:
            QTimer.singleShot(150, self.apply_dark_theme)
            self.theme_btn.setIcon(IconFactory.create_icon("sun", size=40))
            self.update_card_icons(is_dark=True)

        self.is_dark_mode = not self.is_dark_mode
    
    def update_card_icons(self, is_dark):
        """تحديث أيقونات وألوان نصوص البطاقات بناءً على الثيم"""
        color = "white" if is_dark else "#2c3e50"
        desc_color = "rgba(255, 255, 255, 0.9)" if is_dark else "#6c757d"
        
        # قائمة البطاقات لتسهيل التحديث
        cards = [
            (self.ocr_card, "search"),
            (self.pdf_card, "file"),
            (self.security_card, "lock")
        ]
        
        for card, icon_name in cards:
            # تحديث الأيقونة
            card.findChild(QLabel, "cardIconLabel").setPixmap(
                IconFactory.create_icon(icon_name, color=color, size=80).pixmap(64, 64))
            
            # تحديث ألوان النصوص (Enforce Stylesheet override)
            card.findChild(QLabel, "cardTitle").setStyleSheet(
                f"color: {color}; background: transparent; font-size: 18px; font-weight: bold;")
            card.findChild(QLabel, "cardDesc").setStyleSheet(
                f"color: {desc_color}; background: transparent; font-size: 13px;")
    
    def animate_theme_transition(self):
        """تأثير انتقالي سلس عند تغيير الثيم"""
        effect = QGraphicsOpacityEffect(self)
        self.centralWidget().setGraphicsEffect(effect)
        
        fade_out = QPropertyAnimation(effect, b"opacity")
        fade_out.setDuration(150)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.7)
        fade_out.setEasingCurve(QEasingCurve.InOutQuad)
        
        fade_in = QPropertyAnimation(effect, b"opacity")
        fade_in.setDuration(150)
        fade_in.setStartValue(0.7)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.InOutQuad)
        
        fade_out.finished.connect(fade_in.start)
        fade_out.start()
        
        # حفظ الأنيميشن
        self._theme_animation = fade_out
        self._theme_animation2 = fade_in

    def apply_light_theme(self):
        """تطبيق الوضع النهاري"""
        self.setStyleSheet(LIGHT_STYLESHEET)

    def apply_dark_theme(self):
        """تطبيق الوضع الليلي"""
        self.setStyleSheet(DARK_STYLESHEET)
    


    def show_credits(self):
        """عرض نافذة حقوق التطوير"""
        dialog = CreditsDialog(self)
        dialog.exec()

    def show_custom_message(self, title, message, icon_type="info", duration=3000):
        """عرض إشعار احترافي ينزلق من الجانب"""
        popup = NotificationPopup(f"{title}\n{message}", icon_type=icon_type, duration=duration, parent=self)
        popup.show_notification()

    def show_progress_dialog(self):
        """عرض نافذة التقدم"""
        self.progress_dialog = ProgressDialog(self)
        self.progress_dialog.cancel_btn.clicked.connect(self.stop_ocr)
        self.progress_dialog.show()

        # وضع النافذة في وسط الشاشة
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.progress_dialog.width()) // 2
        y = (screen_geometry.height() - self.progress_dialog.height()) // 2
        self.progress_dialog.move(x, y)

    def close_progress_dialog(self):
        """إغلاق نافذة التقدم"""
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None

    def drag_enter_event(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def drop_event(self, event: QDropEvent):
        urls = event.mimeData().urls()
        files = [url.toLocalFile() for url in urls if url.isLocalFile()]
        self.handle_files_selected(files)

    def choose_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "اختر ملفات PDF أو صور",
            "",
            "PDF & Images (*.pdf *.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        self.handle_files_selected(files)

    def handle_files_selected(self, files):
        if files:
            self.current_files = files
            self.update_file_list()
            self.show_custom_message("تم اختيار الملفات", f"تم اختيار {len(files)} ملف", "success")

    def update_file_list(self):
        count = len(self.current_files)

        if count == 0:
            self.file_list_label.setText("لم يتم اختيار ملفات بعد.")
        else:
            file_names = f"✓ تم اختيار {count} ملف:\n\n"
            file_names += "\n".join([f"• {Path(f).name}" for f in self.current_files[:5]])
            if count > 5:
                file_names += f"\n\n... و {count - 5} ملفات أخرى"
            self.file_list_label.setText(file_names)
            self.file_list_label.setStyleSheet("color: #10b981; font-size: 12px; padding: 10px; font-weight: 500;")

    def start_ocr(self):
        if not self.current_files:
            self.show_custom_message("خطأ", "الرجاء اختيار ملفات أولاً", "error")
            return

        if self.ocr_thread and self.ocr_thread.isRunning():
            self.show_custom_message("تحذير", "هناك عملية تحويل قيد التشغيل بالفعل", "warning")
            return

        # Get settings
        lang_map = {"عربي + إنجليزي": "ara+eng", "فقط عربي": "ara", "فقط إنجليزي": "eng"}
        lang = lang_map[self.lang_combo.currentText()]
        dpi = int(self.dpi_spin.text() or "300")
        start_page = int(self.start_page_spin.text() or "1")
        end_page = int(self.end_page_spin.text()) if self.end_page_spin.text() else None
        preprocess = self.preprocess_check.isChecked()

        # Reset UI
        self.text_edit.clear()
        self.progress_bar.setValue(0)
        self.page_stats_label.setText("0 صفحة")
        self.time_stats_label.setText("الوقت: 00:00")
        self.current_page_label.setText("جاري بدء عملية التحويل...")
        self.current_page_label.setStyleSheet(
            "background-color: #FFF9C4; color: #000; padding: 5px; border-radius: 3px;")

        # تعطيل عناصر التحكم أثناء المعالجة
        self.set_controls_enabled(False)

        # عرض نافذة التقدم
        self.show_progress_dialog()

        # Setup worker and thread
        self.ocr_worker = OCRWorker()
        self.ocr_thread = QThread()

        self.ocr_worker.moveToThread(self.ocr_thread)

        # Connect signals
        self.ocr_worker.progress.connect(self.handle_progress)
        self.ocr_worker.finished.connect(self.handle_finished)
        self.ocr_worker.error.connect(self.handle_error)
        self.ocr_worker.log.connect(self.handle_log)
        self.ocr_worker.page_started.connect(self.handle_page_started)

        self.ocr_thread.started.connect(
            lambda: self.ocr_worker.run_ocr(
                self.current_files, lang, dpi, start_page, end_page, True, preprocess
            )
        )

        # Start thread
        self.ocr_thread.start()

        # Update UI
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def handle_page_started(self, message):
        """التعامل مع بدء معالجة صفحة جديدة"""
        self.current_page_label.setText(message)
        self.current_page_label.setStyleSheet(
            "background-color: #E3F2FD; color: #000; padding: 5px; border-radius: 3px;")

    # --- PDF Tools Logic ---

    def choose_merge_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "اختر ملفات PDF لدمجها", "", "PDF Files (*.pdf)")
        if files:
            current_text = self.merge_list.toPlainText().strip()
            if current_text:
                new_text = current_text + "\n" + "\n".join(files)
            else:
                new_text = "\n".join(files)
            self.merge_list.setPlainText(new_text)

    def run_merge(self):
        files = self.merge_list.toPlainText().strip().split("\n")
        if not files or files == ['']:
            self.show_custom_message("تنبيه", "الرجاء إضافة ملفات للدمج أولاً", "warning")
            return
        
        output_path, _ = QFileDialog.getSaveFileName(self, "حفظ الملف المدمج", "merged_document.pdf", "PDF Files (*.pdf)")
        if output_path:
            success, msg = PDFProcessor.merge_pdfs(files, output_path)
            if success:
                self.show_custom_message("نجاح", msg, "success")
                self.merge_list.clear()
            else:
                self.show_custom_message("خطأ", f"فشل الدمج: {msg}", "error")

    def choose_split_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "اختر ملف PDF للفصل", "", "PDF Files (*.pdf)")
        if file:
            self.split_file_input.setText(file)

    def toggle_split_range(self, state):
        """تعطيل أو تمكين مدخل النطاق بناءً على خيار فصل كل صفحة"""
        is_checked = state == Qt.Checked.value
        self.split_range_input.setEnabled(not is_checked)
        if is_checked:
            self.split_range_input.setPlaceholderText("سيتم فصل جميع الصفحات...")
        else:
            self.split_range_input.setPlaceholderText("")

    def run_split(self):
        file = self.split_file_input.text()
        range_str = self.split_range_input.text()
        split_each = self.split_each_page_check.isChecked()
        
        if not file:
            self.show_custom_message("تنبيه", "الرجاء اختيار ملف أولاً", "warning")
            return
            
        if not split_each and not range_str:
            self.show_custom_message("تنبيه", "الرجاء تحديد نطاق الصفحات أو اختيار فصل كل صفحة", "warning")
            return
            
        output_dir = QFileDialog.getExistingDirectory(self, "اختر مجلد الحفظ")
        if output_dir:
            if split_each:
                success, msg = PDFProcessor.split_pdf_to_pages(file, output_dir)
            else:
                success, msg = PDFProcessor.split_pdf(file, output_dir, range_str)
                
            if success:
                self.show_custom_message("نجاح", msg, "success")
            else:
                self.show_custom_message("خطأ", msg, "error")

    # --- Security Logic ---

    def choose_lock_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "اختر ملف PDF للقفل", "", "PDF Files (*.pdf)")
        if file:
            self.lock_file_input.setText(file)

    def run_encrypt(self):
        file = self.lock_file_input.text()
        password = self.lock_pass_input.text()
        if not file or not password:
            self.show_custom_message("تنبيه", "الرجاء اختيار ملف وإدخال كلمة مرور", "warning")
            return
            
        output_path, _ = QFileDialog.getSaveFileName(self, "حفظ الملف المحمي", "protected_document.pdf", "PDF Files (*.pdf)")
        if output_path:
            success, msg = PDFProcessor.encrypt_pdf(file, password, output_path)
            if success:
                self.show_custom_message("نجاح", msg, "success")
                self.lock_pass_input.clear()
            else:
                self.show_custom_message("خطأ", msg, "error")

    def choose_unlock_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "اختر ملف PDF المحمي", "", "PDF Files (*.pdf)")
        if file:
            self.unlock_file_input.setText(file)

    def run_decrypt(self):
        file = self.unlock_file_input.text()
        password = self.unlock_pass_input.text()
        if not file or not password:
            self.show_custom_message("تنبيه", "الرجاء اختيار ملف وإدخال كلمة المرور الحالية", "warning")
            return
            
        output_path, _ = QFileDialog.getSaveFileName(self, "حفظ النسخة المفتوحة", "unlocked_document.pdf", "PDF Files (*.pdf)")
        if output_path:
            success, msg = PDFProcessor.decrypt_pdf(file, password, output_path)
            if success:
                self.show_custom_message("نجاح", msg, "success")
                self.unlock_pass_input.clear()
            else:
                self.show_custom_message("خطأ", msg, "error")

    def stop_ocr(self):
        if self.ocr_worker:
            self.ocr_worker.stop()
        if self.ocr_thread and self.ocr_thread.isRunning():
            self.ocr_thread.quit()
            self.ocr_thread.wait()

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.current_page_label.setText("تم إيقاف عملية التحويل")
        self.current_page_label.setStyleSheet(
            "background-color: #FFEBEE; color: #000; padding: 5px; border-radius: 3px;")
        self.set_controls_enabled(True)

        # إغلاق نافذة التقدم
        self.close_progress_dialog()

        self.show_custom_message("تم الإيقاف", "تم إيقاف عملية التحويل", "warning")

    def handle_progress(self, data):
        progress = int((data["page"] / data["total"]) * 100)
        self.progress_bar.setValue(progress)

        # تحديث نافذة التقدم
        if self.progress_dialog:
            self.progress_dialog.update_progress(progress)

        self.page_stats_label.setText(f"{data['page']} من {data['total']} صفحة")
        self.time_stats_label.setText(f"الوقت: {data['elapsed']}s")

        # Append text
        current_text = self.text_edit.toPlainText()
        self.text_edit.setPlainText(current_text + data["text_preview"])

        # Update stats
        self.update_text_stats()

    def handle_finished(self, data):
        self.progress_bar.setValue(100)
        self.current_page_label.setText("اكتملت عملية التحويل بنجاح!")
        self.current_page_label.setStyleSheet(
            "background-color: #E8F5E9; color: #000; padding: 5px; border-radius: 3px;")

        # إغلاق نافذة التقدم
        self.close_progress_dialog()

        # عرض رسالة النجاح
        self.show_custom_message("تم الانتهاء",
                                 f"تم تحويل {data['total_pages']} صفحة بنجاح في {data['processing_time']} ثانية",
                                 "success")

        # Update final text
        self.text_edit.setPlainText(data["text_preview"])
        self.update_text_stats()

        # Cleanup
        self.ocr_thread.quit()
        self.ocr_thread.wait()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.set_controls_enabled(True)

    def handle_error(self, message):
        self.current_page_label.setText("حدث خطأ أثناء التحويل")
        self.current_page_label.setStyleSheet(
            "background-color: #FFEBEE; color: #000; padding: 5px; border-radius: 3px;")

        # إغلاق نافذة التقدم
        self.close_progress_dialog()

        self.show_custom_message("خطأ", message, "error")
        self.stop_ocr()

    def handle_log(self, message):
        # يمكن إضافة سجل إذا لزم الأمر
        pass

    def set_controls_enabled(self, enabled):
        """تمكين أو تعطيل عناصر التحكم"""
        self.lang_combo.setEnabled(enabled)
        self.dpi_spin.setEnabled(enabled)
        self.start_page_spin.setEnabled(enabled)
        self.end_page_spin.setEnabled(enabled)
        self.preprocess_check.setEnabled(enabled)
        self.theme_btn.setEnabled(enabled)
        self.credits_btn.setEnabled(enabled)
        self.drop_label.setEnabled(enabled)

    def update_text_stats(self):
        text = self.text_edit.toPlainText()
        words = len(text.split())
        chars = len(text)
        self.word_count_label.setText(f"{words} كلمة")
        self.char_count_label.setText(f"{chars} حرف")

    def copy_text(self):
        text = self.text_edit.toPlainText()
        if text.strip():
            QApplication.clipboard().setText(text)
            self.show_custom_message("تم النسخ", "تم نسخ النص إلى الحافظة", "success")
        else:
            self.show_custom_message("تحذير", "لا يوجد نص للنسخ", "warning")

    def save_text(self):
        text = self.text_edit.toPlainText()
        if not text.strip():
            self.show_custom_message("تحذير", "لا يوجد نص للحفظ", "warning")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "حفظ النص المستخرج",
            "extracted_text.txt",
            "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.show_custom_message("تم الحفظ", f"تم حفظ الملف: {file_path}", "success")
            except Exception as e:
                self.show_custom_message("خطأ", f"فشل في حفظ الملف: {e}", "error")

    def show_help(self):
        help_text = """
        <h3>الملفات المدعومة</h3>
        <ul>
            <li>PDF ممسوحة أو تحتوي نص وصور</li>
            <li>صور: PNG, JPG, JPEG, BMP, TIFF</li>
        </ul>

        <h3>نصائح جودة OCR</h3>
        <ul>
            <li>استخدم DPI بين 300–400 للوثائق المطبوعة</li>
            <li>فعّل خيار المعالجة المسبقة لتحسين دقة النصوص العربية</li>
            <li>لملفات ضخمة، جرّب نطاق صفحات جزئي للتجربة أولاً</li>
            <li>استخدم صور عالية الجودة بدقة 300 نقطة/بوصة على الأقل</li>
        </ul>
        """

        self.show_custom_message("مساعدة", "الملفات المدعومة:\n- PDF ممسوحة أو تحتوي نص وصور\n- صور: PNG, JPG, JPEG, BMP, TIFF\n\nنصائح جودة OCR:\n- استخدم DPI بين 300–400\n- فعّل المعالجة المسبقة لتحسين دقة النصوص العربية\n- لملفات ضخمة، جرّب نطاق صفحات جزئي\n- استخدم صور عالية الجودة", "info", duration=6000)


    def closeEvent(self, event):
        if self.ocr_thread and self.ocr_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "تأكيد الإغلاق",
                "هناك عملية تحويل قيد التشغيل. هل تريد الإغلاق على أي حال؟",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.stop_ocr()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()