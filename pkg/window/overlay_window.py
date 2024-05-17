import sys
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QDialog, QVBoxLayout
from PySide6.QtGui import QPixmap

import objc
from AppKit import NSApplication, NSWindowCollectionBehaviorCanJoinAllSpaces, NSWorkspace
from Quartz import kCGScreenSaverWindowLevel

class OverlayWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Overlay Window")
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        self.setFixedSize(300, 200)

        self.background_label = QLabel(self)
        pixmap = QPixmap("images/eve.jpeg")
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.setWindowOpacity(0.75)

        self.background_label.setStyleSheet("border: 5px solid red;")  

        self._drag_active = False
        self._drag_start_pos = QPoint()

        QTimer.singleShot(0, self.make_window_stay_on_all_spaces)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self._drag_active = True
            self._drag_start_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_active:
            self.move(event.globalPos() - self._drag_start_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self._drag_active = False
            event.accept()

    def make_window_stay_on_all_spaces(self):
        window_handle = self.winId()
        qns_view = objc.objc_object(c_void_p=window_handle)
        ns_window = qns_view.window()

        ns_window.setCollectionBehavior_(NSWindowCollectionBehaviorCanJoinAllSpaces)

        ns_window.setLevel_(kCGScreenSaverWindowLevel)
