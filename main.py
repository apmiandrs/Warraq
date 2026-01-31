# -*- coding: utf-8 -*-
import sys
import logging
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QTimer

from ui.main_window import MainWindow
from core.utils import setup_logging
from core.config import BASE_DIR, LOG_FILE, VERSION


def main():
    try:
        # 1. إعداد السجلات
        setup_logging()

        # 2. إنشاء التطبيق
        app = QApplication(sys.argv)
        app.setApplicationName("Warraq")
        app.setApplicationVersion(VERSION)
        
        # 3. إعداد أيقونة البرنامج
        icon_path = str(BASE_DIR / "warraq.png")
        app.setWindowIcon(QIcon(icon_path))

        # 4. إظهار شاشة التحميل (Splash Screen)
        pixmap = QPixmap(icon_path)
        # تصغير الصورة لشاشة التحميل إذا كانت كبيرة جداً
        splash_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        splash = QSplashScreen(splash_pixmap)
        splash.show()
        
        # معالجة الأحداث للتأكد من ظهورها
        app.processEvents()

        # 5. تهيئة النافذة الرئيسية
        window = MainWindow()
        
        # 6. إغلاق شاشة التحميل عند ظهور البرنامج
        QTimer.singleShot(1500, lambda: (window.show(), splash.finish(window)))

        sys.exit(app.exec())
    except Exception as e:
        print(f"خطأ في تشغيل التطبيق: {e}")
        logging.error(f"خطأ في تشغيل التطبيق: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
