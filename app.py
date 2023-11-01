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

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QApplication

import resources_rc
import mainwindow_ui


class MainWindow(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = mainwindow_ui.Ui_Form()
        self.ui.setupUi(self)

        self.setWindowTitle("Python ♥ Qt")
        self.setWindowIcon(QIcon(":/icons/box.svg"))

        self.ui.pushButton.clicked.connect(self.increment)
        self.ui.pushButton_2.clicked.connect(self.decrement)
        self.ui.pushButton_3.clicked.connect(self.reset)

        self.init_members()

    def init_members(self):
        self.label_value = 0

    def increment(self):
        self.label_value += 1
        self.update_label()

    def decrement(self):
        self.label_value -= 1
        self.update_label()

    def reset(self):
        self.label_value = 0
        self.update_label()

    def update_label(self):
        self.ui.label.setText(str(self.label_value))


if __name__ != "__main__":
    sys.exit(1)

app = QApplication(sys.argv)

mw = MainWindow()
mw.show()

app.exec()
