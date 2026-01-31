# -*- coding: utf-8 -*-
from PySide6.QtGui import QIcon, QPainter, QPixmap, QPainterPath, QColor, QPen, QBrush
from PySide6.QtCore import Qt, QSize, QRectF

class IconFactory:
    """مصنع لإنشاء أيقونات احترافية باستخدام QPainterPath"""
    
    @staticmethod
    def create_icon(icon_type, color="#ffffff", size=64):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        path = QPainterPath()
        pen = QPen(QColor(color))
        pen.setWidthF(size / 16)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        
        margin = size * 0.15
        s = size - 2 * margin
        
        if icon_type == "home":
            # رسم منزل
            path.moveTo(margin, margin + s * 0.6)
            path.lineTo(margin + s * 0.5, margin)
            path.lineTo(margin + s, margin + s * 0.6)
            path.lineTo(margin + s, margin + s)
            path.lineTo(margin + s * 0.6, margin + s)
            path.lineTo(margin + s * 0.6, margin + s * 0.6)
            path.lineTo(margin + s * 0.4, margin + s * 0.6)
            path.lineTo(margin + s * 0.4, margin + s)
            path.lineTo(margin, margin + s)
            path.closeSubpath()
            
        elif icon_type == "moon":
            # رسم هلال
            rect = QRectF(margin, margin, s, s)
            path.arcMoveTo(rect, 30)
            path.arcTo(rect, 30, 300)
            inner_rect = QRectF(margin + s * 0.2, margin, s, s)
            path.arcTo(inner_rect, 330, -300)
            path.closeSubpath()
            
        elif icon_type == "sun":
            # رسم شمس
            center_x, center_y = size / 2, size / 2
            radius = s * 0.3
            path.addEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
            
            # أشعة الشمس
            ray_len = s * 0.15
            for i in range(8):
                angle = i * 45
                import math
                rad = math.radians(angle)
                x1 = center_x + math.cos(rad) * (radius + s * 0.05)
                y1 = center_y + math.sin(rad) * (radius + s * 0.05)
                x2 = center_x + math.cos(rad) * (radius + s * 0.05 + ray_len)
                y2 = center_y + math.sin(rad) * (radius + s * 0.05 + ray_len)
                path.moveTo(x1, y1)
                path.lineTo(x2, y2)
                
        elif icon_type == "info":
            # رسم علامة معلومات
            rect = QRectF(margin, margin, s, s)
            path.addEllipse(rect)
            path.moveTo(size/2, size/2 - s*0.1)
            path.lineTo(size/2, size/2 + s*0.3)
            # النقطة بالأعلى
            path.addEllipse(size/2 - 2, size/2 - s*0.3, 4, 4)
            
        elif icon_type == "search":
            # رسم عدسة بحث
            circle_radius = s * 0.35
            path.addEllipse(margin, margin, circle_radius * 2, circle_radius * 2)
            path.moveTo(margin + circle_radius * 1.7, margin + circle_radius * 1.7)
            path.lineTo(margin + s, margin + s)
            
        elif icon_type == "file":
            # رسم ملف مع زاوية مطوية
            path.moveTo(margin, margin)
            path.lineTo(margin + s * 0.7, margin)
            path.lineTo(margin + s, margin + s * 0.3)
            path.lineTo(margin + s, margin + s)
            path.lineTo(margin, margin + s)
            path.closeSubpath()
            path.moveTo(margin + s * 0.7, margin)
            path.lineTo(margin + s * 0.7, margin + s * 0.3)
            path.lineTo(margin + s, margin + s * 0.3)
            
        elif icon_type == "lock":
            # رسم قفل
            body_rect = QRectF(margin, margin + s * 0.4, s, s * 0.6)
            path.addRoundedRect(body_rect, 4, 4)
            shackle_rect = QRectF(margin + s * 0.2, margin, s * 0.6, s * 0.8)
            path.moveTo(margin + s * 0.2, margin + s * 0.4)
            path.arcTo(shackle_rect, 180, -180)
            path.lineTo(margin + s * 0.8, margin + s * 0.4)
            
        elif icon_type == "check":
            # رسم علامة صح
            path.moveTo(margin + s * 0.2, margin + s * 0.5)
            path.lineTo(margin + s * 0.45, margin + s * 0.75)
            path.lineTo(margin + s * 0.85, margin + s * 0.25)
            
        elif icon_type == "x":
            # رسم علامة خطأ
            path.moveTo(margin + s * 0.2, margin + s * 0.2)
            path.lineTo(margin + s * 0.8, margin + s * 0.8)
            path.moveTo(margin + s * 0.8, margin + s * 0.2)
            path.lineTo(margin + s * 0.2, margin + s * 0.8)
            
        elif icon_type == "alert":
            # رسم علامة تنبيه (مثلث)
            path.moveTo(margin + s * 0.5, margin)
            path.lineTo(margin, margin + s)
            path.lineTo(margin + s, margin + s)
            path.closeSubpath()
            path.moveTo(margin + s * 0.5, margin + s * 0.3)
            path.lineTo(margin + s * 0.5, margin + s * 0.7)
            path.addEllipse(margin + s * 0.5 - 1, margin + s * 0.85, 2, 2)

        painter.drawPath(path)
        painter.end()
        return QIcon(pixmap)
