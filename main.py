import sys

from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction, QPixmap, QIcon

from pkg.window import *
from pkg.manager import *

eve_windows = get_open_eve_windows()

for window in eve_windows:
    focus_eve_window(window.pid)

qt_app = QApplication(sys.argv)

qt_window = MainWindow()

qt_overlay = OverlayWindow()
qt_overlay.show()
qt_window.show()
qt_app.exec()
