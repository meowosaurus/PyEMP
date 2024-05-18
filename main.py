import sys

from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction, QPixmap, QIcon

from pkg.window import *
from pkg.manager import *

qt_app = QApplication(sys.argv)

eve_windows = get_open_eve_windows()

overlays = []

for window in eve_windows:
    qt_overlay = OverlayWindow()
    qt_overlay.pid = window.pid
    qt_overlay.show()
    overlays.append(qt_overlay)

qt_window = MainWindow()

qt_window.show()
qt_app.exec()
