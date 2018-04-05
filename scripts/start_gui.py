import sys


def main():
    from qtpy import QtWidgets
    from gui_template.core import GUIMainWindow
    app = QtWidgets.QApplication(sys.argv)
    window = GUIMainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
