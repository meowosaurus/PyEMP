import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QToolBar, QToolButton, QWidgetAction
from PySide6.QtGui import QAction, QIcon, Qt
from PySide6.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyEMP")

        screen = QApplication.primaryScreen()
        screen_size = screen.size()

        self.resize(screen_size.width() / 2, screen_size.height() / 2)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.label = QLabel("Select an action from the toolbar", self)
        main_layout.addWidget(self.label)

        self.toolbar = QToolBar("Main Toolbar", self)
        self.toolbar.setIconSize(QSize(25, 25))
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)
        self.toolbar.setFixedWidth(screen_size.width() // 10)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        self.add_toolbar_actions()

    def button_clicked(self):
        self.label.setText("Button Clicked!")

    def add_toolbar_actions(self):
        self.toolbar.addAction(self.create_tool_button("images/icon.png", "General", "General selected"))
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.create_tool_button("images/icon.png", "Appearance", "Appearance selected"))
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.create_tool_button("images/icon.png", "About", "About selected"))

    def create_tool_button(self, icon_path, text, message):
        button = QToolButton()
        button.setIcon(QIcon(icon_path))
        button.setText(text)
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        button.setFixedWidth(150)
        button.setStyleSheet("QToolButton { text-align: left; padding-left: 10px; }")
        button.clicked.connect(lambda: self.label.setText(message))

        action = QWidgetAction(self)
        action.setDefaultWidget(button)
        return action