import sys
from PySide6.QtWidgets import QApplication
from overlay import Overlay

app = QApplication(sys.argv)
overlay = Overlay()
overlay.update_text("test")
sys.exit(app.exec())