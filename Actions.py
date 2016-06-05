
import os, time
from PyQt4 import QtGui, QtCore

import ChromecastConverter
from Widgets import *

class Actions(QtCore.QObject):
    def __init__(self, parent = None):
        super(Actions, self).__init__(parent)
        self.mainWidget = parent

    @QtCore.pyqtSlot(list)
    def updateOutputsListAction(self,fileList=[]):
        if fileList == []:
            widget = self.mainWidget.inputsPane.fileListWidget
            for i in range(0,widget.count()):
                item = widget.item(i)
                fileList.append(str(item.text()))
            self.mainWidget.outputsPane.fileListWidget.clear()
        fullPathBox = self.mainWidget.outputsPane.filePathCheckbox.isChecked()
        for fileName in fileList:
            outputPathLocation = self.mainWidget.outputsPane.outputLocationTextbox.text()
            if fullPathBox:
                outputFileName = '/'.join([str(outputPathLocation),str(fileName)]).replace('//','/')
            else:
                outputFileName = str(fileName).split('/')[-1]
            outputListWigetItem = OutputListWidgetItem(outputFileName)
            self.mainWidget.outputsPane.fileListWidget.addItem(outputListWigetItem)
        if not fileList:
            self.mainWidget.outputsPane.fileListWidget.clear()

    @QtCore.pyqtSlot(int)
    def updateFullPath(self,state):
        fileList = []
        widget = self.mainWidget.inputsPane.fileListWidget
        for i in range(0,widget.count()):
            item = widget.item(i)
            fileList.append(str(item.text()))
        self.mainWidget.outputsPane.fileListWidget.clear()
        fullPathBox = self.mainWidget.outputsPane.filePathCheckbox.isChecked()
        for fileName in fileList:
            outputPathLocation = self.mainWidget.outputsPane.outputLocationTextbox.text()
            if fullPathBox:
                outputFileName = '/'.join([str(outputPathLocation),str(fileName).split('/')[-1]]).replace('//','/')
            else:
                outputFileName = str(fileName).split('/')[-1]
            outputListWigetItem = OutputListWidgetItem(outputFileName)
            self.mainWidget.outputsPane.fileListWidget.addItem(outputListWigetItem)
        if not fileList:
            self.mainWidget.outputsPane.fileListWidget.clear()    

    @QtCore.pyqtSlot(QtCore.QString)
    def updatePathLocation(self,path):
        fileList = []
        widget = self.mainWidget.inputsPane.fileListWidget
        for i in range(0,widget.count()):
            item = widget.item(i)
            fileList.append(str(item.text()))
        self.mainWidget.outputsPane.fileListWidget.clear()
        fullPathBox = self.mainWidget.outputsPane.filePathCheckbox.isChecked()
        for fileName in fileList:
            outputPathLocation = self.mainWidget.outputsPane.outputLocationTextbox.text()
            if fullPathBox:
                outputFileName = '/'.join([str(outputPathLocation),str(fileName).split('/')[-1]]).replace('//','/')
            else:
                outputFileName = str(fileName).split('/')[-1]
            outputListWigetItem = OutputListWidgetItem(outputFileName)
            self.mainWidget.outputsPane.fileListWidget.addItem(outputListWigetItem)
        if not fileList:
            self.mainWidget.outputsPane.fileListWidget.clear() 

    def getFileList(self):
        fileList = []
        rowCount = self.mainWidget.inputsPane.fileListWidget.count()
        checkBoxValue = self.mainWidget.outputsPane.filePathCheckbox.isChecked()
        aQual = self.mainWidget.dockPane.audioGroupBox.getOptions()
        vQual,fileExt = self.mainWidget.dockPane.videoGroupBox.getOptions()
        for i in range(rowCount):
            inputRowItem = str(self.mainWidget.inputsPane.fileListWidget.item(i).text())
            outputRowItem = str(self.mainWidget.outputsPane.fileListWidget.item(i).text())
            if not checkBoxValue:
                path = str(self.mainWidget.outputsPane.outputLocationTextbox.text())
                outputFileName = '/'.join([path,outputRowItem]).replace('//','/')
                outputFileName = os.path.splitext(outputFileName)[0]+'.'+fileExt
            else:
                outputFileName = outputRowItem
                outputFileName = os.path.splitext(outputFileName)[0]+'.'+fileExt
            fileList.append((inputRowItem,outputFileName))

        totalFileCount = len(fileList)
        self.mainWidget.progressBar.reset()
        self.mainWidget.progressBar.setRange(1,totalFileCount)
        self.convertFiles(fileList)

    def convertFiles(self,fileList):
        aQual = self.mainWidget.dockPane.audioGroupBox.getOptions()
        vQual,fileExt = self.mainWidget.dockPane.videoGroupBox.getOptions()

        kwargs = {
            "fileList" : fileList,
            "audioQuality" : aQual,
            "videoQuality" : vQual,
        }

        self.convertThread = ConverterThread(**kwargs)
        self.convertThread.updateProgressbar.connect(self.updateProgressbar)
        self.convertThread.updateStatusbar.connect(self.updateStatusbar)
        self.convertThread.finished.connect(self.enableWidgets)
        # self.convertThread.run(**kwargs)
        self.convertThread.start()
        self.disableWidgets()

        # items = (self.mainWidget.main_layout.itemAt(i) for i in range(self.mainWidget.main_layout.count())) 
        # for w in items:
        #     print w

    def updateProgressbar(self,value):
        self.mainWidget.progressBar.setValue(value)
        QtGui.QApplication.processEvents()

    def updateStatusbar(self,message):
        self.mainWidget.messageBar.showMessage(message)
        QtGui.QApplication.processEvents()

    def skippedProcess(self):
        self.convertThread.terminate()
        msg = "Process Skipped!"
        self.mainWidget.messageBar.showMessage(msg)
        self.enableWidgets()

    def disableWidgets(self):
        self.mainWidget.inputsPane.setEnabled(False)
        self.mainWidget.outputsPane.setEnabled(False)
        self.mainWidget.dockPane.setEnabled(False)
        self.mainWidget.processButton.setText('Abort!')
        self.mainWidget.processButton.released.connect(self.skippedProcess)

    def enableWidgets(self):
        self.mainWidget.inputsPane.setEnabled(True)
        self.mainWidget.outputsPane.setEnabled(True)
        self.mainWidget.dockPane.setEnabled(True)
        self.mainWidget.processButton.setText('Process')
        self.mainWidget.processButton.released.connect(self.getFileList)

class ConverterThread(QtCore.QThread):
    updateProgressbar = QtCore.pyqtSignal(int)
    updateStatusbar = QtCore.pyqtSignal(str)

    def __init__(self, parent=None,*args,**kwargs):
        super(ConverterThread, self).__init__(parent)

        self.Converter = ChromecastConverter.Converter(listeners=[self.updateStatus])
        self.fileList = kwargs['fileList']
        self.aQual = kwargs['audioQuality']
        self.vQual = kwargs['videoQuality']

    def run(self,*args,**kwargs):
        for i, files in enumerate(self.fileList):
            inFile,outFile = files
            self.Converter.convertFile(inFile,outFile,self.aQual,self.vQual)
            self.updateProgressbar.emit(i+1)
            msg = "Complete: %s"%outFile
            self.updateStatusbar.emit(msg)
        self.updateProgressbar.emit(len(self.fileList))
        self.updateStatusbar.emit('Converstion Complete')
        # self.finished.emit()
        pass

    def updateStatus(self,message):
        self.updateStatusbar.emit(message)

    def terminate(self):
        self.Converter.childProcess.kill()
        self.quit()

