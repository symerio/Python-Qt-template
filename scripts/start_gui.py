import sys

from qtpy import QtWidgets
from gui_template.core import SymerioMainWindow

print('OK')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = SymerioMainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
