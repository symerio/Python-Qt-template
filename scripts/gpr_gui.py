#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from siqt import QtWidgets

from tagui.core import GprMainWindow



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GprMainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
