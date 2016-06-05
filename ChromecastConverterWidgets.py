
import sys, os
from PyQt4 import QtGui, QtCore, Qt

USER = os.getenv("USER")

class InputsPane(QtGui.QGroupBox):
    updateOutputsList = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(InputsPane, self).__init__(parent)

        main_layout = QtGui.QVBoxLayout()

        self.fileListWidget = QtGui.QListWidget()
        
        self.clearButton = QtGui.QPushButton("Clear All")
        self.removeSelectedButton = QtGui.QPushButton("Remove Selected")
        self.browseButton = QtGui.QPushButton('Browse')
        
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(self.clearButton)
        buttonLayout.addWidget(self.removeSelectedButton)
        buttonLayout.addWidget(self.browseButton)
        self.clearButton.released.connect(self.clearAction)
        self.removeSelectedButton.released.connect(self.removeSelectedAction)
        self.browseButton.released.connect(self.showFileDialog)

        main_layout.addWidget(self.fileListWidget)
        main_layout.addLayout(buttonLayout)

        self.setLayout(main_layout)

    def showFileDialog(self):
        userPath = '/Users/%s/Desktop'%USER
        dialog = QtGui.QFileDialog.getOpenFileNames(self, "Select movie files to convert",userPath)
        outputFiles = []
        for fname in dialog:
            fileName = str(fname).split('/')[-1]
            listWidgetItem = QtGui.QListWidgetItem(fname)
            self.fileListWidget.addItem(listWidgetItem)
            outputFiles.append(str(fname))
        
        self.updateOutputsList.emit(outputFiles)

    def clearAction(self):
        self.fileListWidget.clear()
        self.updateOutputsList.emit([])

    def removeSelectedAction(self):
        removeItemList = []
        for item in self.fileListWidget.selectedItems():
            index = self.fileListWidget.indexFromItem(item).row()
            i = self.fileListWidget.takeItem(index)
        self.updateOutputsList.emit([])
            
class OutputsPane(QtGui.QGroupBox):
    def __init__(self, parent=None):
        super(OutputsPane, self).__init__(parent)

        main_layout = QtGui.QVBoxLayout()

        self.filePathCheckbox = QtGui.QCheckBox("View Full Path")
        # self.fileListWidget = QtGui.QListWidget()
        self.fileListWidget = OutputListWidget()
        outputLocationLayout = QtGui.QHBoxLayout()
        outputLocationLabel = QtGui.QLabel("Output Location:")
        self.outputLocationTextbox = QtGui.QLineEdit('/Users/%s/Desktop/'%USER)
        self.outputLocationButton = QtGui.QPushButton("Browse")
        self.outputLocationButton.released.connect(self.showFileDialog)

        outputLocationLayout.addWidget(outputLocationLabel)
        outputLocationLayout.addWidget(self.outputLocationTextbox)
        outputLocationLayout.addWidget(self.outputLocationButton)
        
        main_layout.addWidget(self.filePathCheckbox)
        main_layout.addWidget(self.fileListWidget)
        main_layout.addLayout(outputLocationLayout)

        self.setLayout(main_layout)

    def showFileDialog(self):
        userPath = '/Users/%s/Desktop'%USER
        dialog = QtGui.QFileDialog.getExistingDirectory(self, "Select movie files to convert",userPath,QtGui.QFileDialog.ShowDirsOnly)
        self.outputLocationTextbox.setText(dialog)

class OptionsPane(QtGui.QDockWidget):
    def __init__(self, parent=None):
        super(OptionsPane, self).__init__(parent)

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.setFeatures(QtGui.QDockWidget.DockWidgetMovable)

        main_layout = QtGui.QVBoxLayout()

        self.mainWidget = QtGui.QWidget(self)

        self.audioGroupBox = AudioOptions()
        self.videoGroupBox = VideoOptions()

        main_layout.addWidget(self.videoGroupBox)
        main_layout.addWidget(self.audioGroupBox)

        self.mainWidget.setLayout(main_layout)

        self.setWidget(self.mainWidget)

        self.setMinimumWidth(300)
        # self.setLayout(main_layout)

class AudioOptions(QtGui.QGroupBox):
    def __init__(self, parent=None):
        super(AudioOptions, self).__init__(parent)

        self.qualDropDown = QtGui.QComboBox()
        self.populateDropDown()

        main_layout = QtGui.QVBoxLayout()

        main_layout.addWidget(self.qualDropDown)
        main_layout.addStretch(0)

        self.setLayout(main_layout)
        self.setTitle("Audio Options")

    def populateDropDown(self):
        self.qualDropDown.addItem('Highest')
        self.qualDropDown.addItem('Higher')
        self.qualDropDown.addItem('High')
        self.qualDropDown.addItem('Medium')
        self.qualDropDown.addItem('Low')

    def getOptions(self):
        return str(self.qualDropDown.currentText()).lower()

class VideoOptions(QtGui.QGroupBox):
    def __init__(self, parent=None):
        super(VideoOptions, self).__init__(parent)

        self.qualDropDown = QtGui.QComboBox()
        self.extDropDown = QtGui.QComboBox()
        self.populateDropDown()

        main_layout = QtGui.QVBoxLayout()

        qualLayout = QtGui.QHBoxLayout()
        qualLabel = QtGui.QLabel('Quality:')
        qualLayout.addWidget(qualLabel)
        qualLayout.addWidget(self.qualDropDown)
        
        extLayout = QtGui.QHBoxLayout()
        extLabel = QtGui.QLabel('Container:')
        extLayout.addWidget(extLabel)
        extLayout.addWidget(self.extDropDown)

        main_layout.addLayout(qualLayout)
        main_layout.addLayout(extLayout)
        main_layout.addStretch(0)

        self.setLayout(main_layout)
        self.setTitle("Video Options")

    def populateDropDown(self):
        self.qualDropDown.addItem('Highest')
        self.qualDropDown.addItem('Higher')
        self.qualDropDown.addItem('High')
        self.qualDropDown.addItem('Medium')
        self.qualDropDown.addItem('Low')

        self.extDropDown.addItem('mp4')
        self.extDropDown.addItem('mkv')

    def getOptions(self):
        return (str(self.qualDropDown.currentText()).lower(),str(self.extDropDown.currentText()).lower())

class OutputListWidgetItem(QtGui.QListWidgetItem):
    def __init__(self, parent=None):
        super(OutputListWidgetItem, self).__init__(parent)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)

        Action = menu.addAction("I am a " + self.name + " Action")
        Action.triggered.connect(self.printName)

        menu.exec_(event.globalPos())

    def printName(self):
        print "Action triggered from " + self.name

class OutputListWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        super(OutputListWidget, self).__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.customContextMenu)

    def customContextMenu(self, pos):
        # menu = QtGui.QMenu(self)

        # Action = menu.addAction("I am a " + self.name + " Action")
        # Action.triggered.connect(self.printName)

        # menu.exec_(event.globalPos())
        item = self.itemAt(pos)
        if item is not None:
            menu = QtGui.QMenu("Context Menu", self)
            menu.addAction("Rename", self.renameDialog)
            ret = menu.exec_(self.mapToGlobal(pos))
        
    def renameDialog(self):
        newName, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter your name:')
        
        if ok:
            # self.le.setText(str(text))
            print ok,newName
            items = self.selectedItems()
            for item in items:
                item.setText(newName)
            # cursor = QtGui.QCursor()
            # print cursor
            # pos = cursor.pos()
            # print pos
            # widgetItem = self.itemAt(pos)
            # print self, self.itemAt(pos)
            # widgetItem.setText(newName)

    def getNewName(self):
        print "GET NEW NAME"
        pass

class RenameOutputWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(RenameOutputWidget, self).__init__(parent)
        dialogLayout = QtGui.QVBoxLayout()

        renameLabel = QtGui.QLabel("Rename:")
        self.renameLine = QtGui.QLineEdit()

        self.okayButton = QtGui.QPushButton("Ok")
        # okayButton.released.connect(self.getNewName)

        dialogLayout.addWidget(renameLabel)
        dialogLayout.addWidget(self.renameLine)
        dialogLayout.addWidget(self.okayButton)

        self.setLayout(dialogLayout)

class RenameFileInput(QtGui.QWidget):
    
    def __init__(self):
        super(RenameFileInput, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        self.btn = QtGui.QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)
        
        self.le = QtGui.QLineEdit(self)
        self.le.move(130, 22)
        
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        # self.show()
        
    def showDialog(self):
        
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter your name:')
        
        if ok:
            self.le.setText(str(text))
