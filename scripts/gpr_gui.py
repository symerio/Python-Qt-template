#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

os.environ['QT_API'] = 'pyqt'

from qtpy import QtWidgets
from gprkrige.core import GprMainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GprMainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
