import sys

from PyQt6.QtWidgets import QApplication
from gui import MainForm

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainForm.FrmMain()
    window.show()
    app.exec()
