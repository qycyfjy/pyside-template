# nuitka-project: --standalone
# nuitka-project: --onefile
# nuitka-project: --enable-plugin=pyside6
# nuitka-project: --windows-icon-from-ico=box.png
# nuitka-project: --disable-console
# nuitka-project: --lto=yes

try:
    from ctypes import windll

    app_id = "python_demo_app"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
except ImportError:
    pass

import os
import sys
from typing import Optional

from PySide6.QtCore import Signal, Slot, Property
from PySide6.QtGui import QIcon, QAction, QPalette
from PySide6.QtWidgets import (
    QWidget,
    QApplication,
    QSystemTrayIcon,
    QMenu,
    QColorDialog,
)
import pyqtgraph as pg

import resources_rc
import mainwindow_ui


class MainWindow(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = mainwindow_ui.Ui_Form()
        self.ui.setupUi(self)

        self.main_icon = QIcon(":/icons/box.svg")

        self.setWindowTitle("Python ♥ Qt")
        self.setWindowIcon(self.main_icon)

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.main_icon)
        self.tray.setVisible(True)

        self.tray_menu = QMenu()
        self.copy_color_action = QAction("Change Color")
        self.copy_color_action.triggered.connect(self.select_label_color)
        self.tray_menu.addAction(self.copy_color_action)
        self.tray_menu.addSeparator()
        self.exit_action = QAction("Exit")
        self.exit_action.triggered.connect(QApplication.exit)
        self.tray_menu.addAction(self.exit_action)
        self.tray.setContextMenu(self.tray_menu)

        self.ui.pushButton.clicked.connect(self.increment)
        self.ui.pushButton_2.clicked.connect(self.decrement)
        self.ui.pushButton_3.clicked.connect(self.reset)

        self.init_members()

    def init_members(self):
        self._counter = 0
        self.history = [0]

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, value):
        self._counter = value
        self.history.append(self._counter)
        self.update_ui()

    def increment(self):
        self.counter += 1

    def decrement(self):
        self.counter -= 1

    def reset(self):
        self.counter = 0

    def select_label_color(self):
        original_palette = self.ui.label.palette()
        dialog = QColorDialog()
        dialog.currentColorChanged.connect(self.set_label_color)
        if not dialog.exec():
            self.ui.label.setPalette(original_palette)

    def set_label_color(self, color):
        palette = self.ui.label.palette()
        palette.setColor(QPalette.ColorRole.WindowText, color)
        self.ui.label.setPalette(palette)

    def update_ui(self):
        self.ui.label.setText(str(self._counter))
        self.ui.plotting.plot(self.history)


if __name__ != "__main__":
    sys.exit(1)

app = QApplication(sys.argv)

mw = MainWindow()
mw.show()

app.exec()
