#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from ChromecastConverterApp import *


def main():
    
    app = QtGui.QApplication(sys.argv)
    cca = ChromecastConverterApp()
    cca.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()