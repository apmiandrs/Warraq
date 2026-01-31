# -*- coding: utf-8 -*-
import time
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QRect, QSequentialAnimationGroup
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QLinearGradient, QPixmap
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton,
                               QProgressBar, QDialogButtonBox, QHBoxLayout, QWidget,
                               QGraphicsDropShadowEffect, QFrame)
from pathlib import Path
from ui.icon_factory import IconFactory


# ==========================
# إشعارات Popup احترافية محسّنة
# ==========================
class NotificationPopup(QWidget):
    def __init__(self, message, icon_type="info", duration=3000, parent=None):
        super().__init__(parent)
        self.duration = duration
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(380, 100)

        # تحديد الألوان والأيقونات بناءً على النوع
        self.icon_map = {
            "info": {"bg": "#3b82f6", "border": "#2563eb", "icon": "info"},
            "warning": {"bg": "#f59e0b", "border": "#d97706", "icon": "alert"},
            "error": {"bg": "#ef4444", "border": "#dc2626", "icon": "x"},
            "success": {"bg": "#10b981", "border": "#059669", "icon": "check"}
        }
        self.current_data = self.icon_map.get(icon_type, self.icon_map["info"])
        self.current_color = self.current_data

        # الحاوية الرئيسية
        self.container = QFrame(self)
        self.container.setObjectName("notificationContainer")
        self.container.setFixedSize(370, 90)
        
        # تطبيق التصميم
        self.container.setStyleSheet(f"""
            #notificationContainer {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.current_color['bg']}, 
                    stop:1 {self.current_color['border']});
                border-radius: 12px;
                border: 2px solid rgba(255, 255, 255, 0.3);
            }}
            QLabel {{
                color: white;
                background: transparent;
            }}
        """)

        # إضافة ظل متقدم
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 6)
        self.container.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        # أيقونة
        self.icon_label = QLabel()
        self.icon_label.setPixmap(IconFactory.create_icon(self.current_data["icon"], color="white", size=48).pixmap(40, 40))
        self.icon_label.setFixedSize(40, 40)
        layout.addWidget(self.icon_label)

        # الرسالة
        self.message_label = QLabel(message)
        self.message_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.message_label)

        # Animation - Opacity
        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(300)
        self.opacity_anim.setStartValue(0)
        self.opacity_anim.setEndValue(1)
        self.opacity_anim.setEasingCurve(QEasingCurve.OutCubic)

        # Animation - Slide with bounce
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(600)
        self.pos_anim.setEasingCurve(QEasingCurve.OutBack)

        # Timer للإغلاق التلقائي
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close_popup)

    def show_notification(self):
        # حساب الموقع البدائي والنهائي
        screen = self.parent().geometry() if self.parent() else self.screen().geometry()
        end_x = screen.x() + 20
        end_y = screen.y() + screen.height() - self.height() - 40
        start_x = end_x - 100  # Slide from left with more distance
        
        self.move(start_x, end_y)
        self.pos_anim.setStartValue(QPoint(start_x, end_y))
        self.pos_anim.setEndValue(QPoint(end_x, end_y))
        
        super().show()
        self.opacity_anim.start()
        self.pos_anim.start()
        self.timer.start(self.duration)

    def close_popup(self):
        # تأثير الإغلاق
        close_anim = QPropertyAnimation(self, b"windowOpacity")
        close_anim.setDuration(300)
        close_anim.setStartValue(1.0)
        close_anim.setEndValue(0.0)
        close_anim.setEasingCurve(QEasingCurve.InCubic)
        close_anim.finished.connect(self.close)
        close_anim.start()
        
        # حفظ الأنيميشن
        self._close_anim = close_anim


# ==========================
# ProgressDialog محسّن بتصميم عصري
# ==========================
class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_time = time.time()
        self._setup_ui()
        self._setup_timer()
        self._setup_animations()

    def _setup_ui(self):
        self.setWindowTitle("جاري التحويل...")
        self.setFixedSize(450, 250)
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        
        # تطبيق تصميم متدرج
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f0f4f8);
                border: 3px solid qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 15px;
            }
            QLabel {
                color: #2c3e50;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ef4444, stop:1 #dc2626);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #dc2626, stop:1 #b91c1c);
            }
        """)

        # إضافة ظل
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # أيقونة متحركة
        self.icon_label = QLabel()
        self.icon_label.setPixmap(IconFactory.create_icon("search", color="#667eea", size=60).pixmap(48, 48))
        self.icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_label)

        # العنوان
        self.title_label = QLabel("جاري تحويل الملفات...")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setStyleSheet("color: #667eea;")
        layout.addWidget(self.title_label)

        # شريط التقدم المحسّن
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
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
        """)
        layout.addWidget(self.progress_bar)

        # معلومات الوقت
        self.timer_label = QLabel("الوقت المنقضي: 00:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 11))
        self.timer_label.setStyleSheet("color: #6c757d;")
        layout.addWidget(self.timer_label)

        # زر الإلغاء
        self.cancel_btn = QPushButton("⏹ إلغاء التحويل")
        layout.addWidget(self.cancel_btn)

    def _setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def _setup_animations(self):
        """إضافة تأثير حركي للأيقونة"""
        self.icon_animation = QPropertyAnimation(self.icon_label, b"geometry")
        self.icon_animation.setDuration(1000)
        self.icon_animation.setLoopCount(-1)  # تكرار لا نهائي
        self.icon_animation.setEasingCurve(QEasingCurve.InOutSine)
        
        # حركة صعود ونزول بسيطة
        current_geo = self.icon_label.geometry()
        up_geo = current_geo.adjusted(0, -5, 0, -5)
        
        self.icon_animation.setStartValue(current_geo)
        self.icon_animation.setEndValue(up_geo)
        self.icon_animation.start()

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.timer_label.setText(f"الوقت المنقضي: {minutes:02d}:{seconds:02d}")

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        
        # تغيير الأيقونة بناءً على التقدم
        if value < 30:
            self.icon_label.setPixmap(IconFactory.create_icon("search", color="#667eea", size=60).pixmap(48, 48))
        elif value < 60:
            self.icon_label.setPixmap(IconFactory.create_icon("file", color="#667eea", size=60).pixmap(48, 48))
        elif value < 90:
            self.icon_label.setPixmap(IconFactory.create_icon("info", color="#667eea", size=60).pixmap(48, 48))
        else:
            self.icon_label.setPixmap(IconFactory.create_icon("check", color="#10b981", size=60).pixmap(48, 48))

    def closeEvent(self, event):
        if hasattr(self, 'timer'):
            self.timer.stop()
        if hasattr(self, 'icon_animation'):
            self.icon_animation.stop()
        super().closeEvent(event)


# ==========================
# CreditsDialog محسّن بتصميم جذاب
# ==========================
class CreditsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("حقوق التطوير")
        self.setFixedSize(500, 350)
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        
        # تطبيق تصميم متدرج
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 20px;
            }
            QLabel {
                color: white;
                background: transparent;
            }
            QPushButton {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.4);
                padding: 10px 30px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.3);
                border: 2px solid white;
            }
        """)

        # إضافة ظل
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 120))
        shadow.setOffset(0, 10)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # أيقونة (الشعار)
        icon_label = QLabel()
        logo_pixmap = QPixmap(str(Path(__file__).parent.parent / "warraq.png"))
        icon_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # العنوان
        title_label = QLabel("المساعد الذكي للملفات")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addWidget(title_label)

        # معلومات المطور
        info_label = QLabel(
            "تم تطوير هذا التطبيق بواسطة:\n\n"
            "م/ عبدالله بن علي الغميز\n\n"
            "برنامج احترافي لاستخراج النصوص من الملفات\n"
            "مع دعم كامل للغة العربية\n\n"
            "الإصدار 2.0.0"
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(QFont("Arial", 12))
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        layout.addStretch()

        # زر الإغلاق
        close_btn = QPushButton("✓ حسناً")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        # تأثير الظهور
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(400)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

    def showEvent(self, event):
        self.animation.start()
        super().showEvent(event)
