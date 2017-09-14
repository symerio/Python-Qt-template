import sys
import os


def main():
    from qtpy import QtWidgets
    from gui_template.core import InsightMainWindow
    app = QtWidgets.QApplication(sys.argv)
    window = InsightMainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    # use pyside2 QT backend by default
    if "QT_API" not in os.environ:
        os.environ['QT_API'] = 'pyside2'
    main()
