
import sys,os
from PyQt4 import QtGui, QtCore, Qt
import Actions
from Widgets import *



class ChromecastConverterApp(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(ChromecastConverterApp, self).__init__(parent)

        self.main_layout = QtGui.QVBoxLayout()
        
        centralWidget = QtGui.QWidget()
        centralWidgetLayout = QtGui.QVBoxLayout()
        
        self.inputsPane = InputsPane('File Inputs:')
        self.outputsPane = OutputsPane('File Outputs:')
        self.dockPane = OptionsPane("Options:")

        progressLayout = QtGui.QHBoxLayout()
        self.processButton = QtGui.QPushButton("Process")
        self.progressBar = QtGui.QProgressBar()
        progressLayout.addWidget(self.progressBar)
        progressLayout.addWidget(self.processButton)

        self.messageBar = self.statusBar()

        centralWidgetLayout.addWidget(self.inputsPane)
        centralWidgetLayout.addWidget(self.outputsPane)
        # centralWidgetLayout.addWidget(self.processButton)
        centralWidgetLayout.addLayout(progressLayout)

        centralWidget.setLayout(centralWidgetLayout)
        self.main_layout.addWidget(centralWidget)
        
        self.setCentralWidget(centralWidget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockPane)
        self.setWindowTitle('ChromecastConverterApp')
        self.resize(800,600)
        self.setGUIActions()

    def setGUIActions(self):
        actions = Actions.Actions(parent=self)

        self.inputsPane.updateOutputsList.connect(actions.updateOutputsListAction)
        self.outputsPane.filePathCheckbox.stateChanged.connect(actions.updateFullPath)
        self.outputsPane.outputLocationTextbox.textChanged.connect(actions.updatePathLocation)

        self.processButton.released.connect(actions.getFileList)
        actions.updateStatusbar("Welcome to ChromecastConverter 1.0")







