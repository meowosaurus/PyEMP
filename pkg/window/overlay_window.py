import sys
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QDialog, QVBoxLayout
from PySide6.QtGui import QPixmap, QImage

import objc
from AppKit import NSWindowCollectionBehaviorCanJoinAllSpaces
from Quartz import kCGScreenSaverWindowLevel

from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionAll, kCGNullWindowID, CGWindowListCreateImage, kCGWindowImageDefault
from AppKit import NSApplication, NSBitmapImageRep

import Quartz
from Quartz.CoreGraphics import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowImageDefault, CGWindowListCreateImage

from Quartz import CGImageDestinationCreateWithData, CGImageDestinationAddImage, CGImageDestinationFinalize
from Foundation import NSMutableData

import io
#from PIL import Image

from ..manager import *

def capture_window_image(window_id):
    # Capture the window image
    image = CGWindowListCreateImage(CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)[0]['kCGWindowBounds'],
                                    kCGWindowListOptionAll, window_id, kCGWindowImageDefault)

    # Convert the image to a format usable by PySide6
    bitmap = NSBitmapImageRep.alloc().initWithCGImage_(image)
    data = bitmap.representationUsingType_properties_(NSBitmapImageRep.NSBitmapImageFileTypePNG, None)
    byte_data = data.bytes()
    byte_array = bytearray(byte_data)

    qimage = QImage()
    qimage.loadFromData(byte_array, "PNG")
    return qimage

class OverlayWindow(QDialog):
    pid = 0

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Overlay Window")
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # TODO: Add option for user to change overlay size
        self.setFixedSize(300, 200)

        # Capture the window's image
        window_image = CGWindowListCreateImage(
            Quartz.CGRectNull, 
            Quartz.kCGWindowListOptionIncludingWindow, 
            self.pid, 
            kCGWindowImageDefault
        )

        # TODO: Copy image from EVE window and insert here
        self.background_label = QLabel(self)
        pixmap = QPixmap("images/eve.jpeg")
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        # TODO: Add option for user to change opacity
        self.setWindowOpacity(0.75)

        # TODO: Add option for user to change size and color
        self.background_label.setStyleSheet("border: 5px solid red;")  

        self._drag_active = False
        self._drag_start_pos = QPoint()

        QTimer.singleShot(0, self.make_window_stay_on_all_spaces)

    def mousePressEvent(self, event):
        # Use left click to focus EVE window
        if event.button() == Qt.LeftButton:
            focus_eve_window(self.pid)
        # Use right click to move the overlay around
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

    # TODO: Doesn't work with fullscreen windows yet
    def make_window_stay_on_all_spaces(self):
        window_handle = self.winId()
        qns_view = objc.objc_object(c_void_p=window_handle)
        ns_window = qns_view.window()

        ns_window.setCollectionBehavior_(NSWindowCollectionBehaviorCanJoinAllSpaces)

        ns_window.setLevel_(kCGScreenSaverWindowLevel)
