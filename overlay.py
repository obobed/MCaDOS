from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QCursor

class Bridge(QObject):
    sequence_changed = Signal(str)

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; background: rgba(0,0,0,160); "
                                 "padding: 4px 8px; border-radius: 6px; font-size: 14px")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.label)
        self.hide()

    def update_text(self, text):
        print(f"update text {text!r}")
        if not text:
            self.hide()
            return
        self.label.setText(text)
        self.resize(self.label.sizeHint())
        self.adjustSize()
        pos = QCursor.pos()
        self.move(pos.x() + 16, pos.y() + 16)
        self.show()
        self.raise_()
        self.activateWindow()