

import sys, os, re, json, subprocess, datetime


CWD = os.path.dirname(os.path.realpath(__file__))
LOGPATH = os.path.join(CWD,'logs')

class Converter(object):
    def __init__(self, *args,**kwargs):
        self.loadConfig()

        if kwargs.has_key('listeners'):
            self.listeners = kwargs['listeners']
        else:
            self.listeners = []

        if kwargs.has_key('logPath'):
            self.logPath = kwargs['logPath']
        else: self.logPath = LOGPATH
        if not os.path.isdir(self.logPath):
            os.mkdir(self.logPath)

    def loadConfig(self):
        f = open(os.path.join(CWD,'config'),'r')
        self.config = json.loads(f.read())
        f.close()

    def checkFile(self,fileName):
        return os.path.isfile(fileName)

    def preprocessCheck(self,inFile,outFile):
        if os.path.isfile(inFile):
            outFileDir = '/'.join(str(outFile).split('/')[:-1])
            if not os.path.isdir(outFileDir):
                msg = "Output directory does not exist: %s" %outFileDir
                raise PreprocessError(message=msg)
        else:
            msg = "File does not exist: %s" %inFile 
            raise PreprocessError(message=msg) 

    def convertFile(self,inFile,outFile,aQual,vQual):
        try:
            self.preprocessCheck(inFile,outFile)
        except PreprocessError as e:
            print e.message
        else:
            acodec = self.config['codec']['audio']['default']
            vcodec = self.config['codec']['video']['default']
            vQuality = self.config['quality']['video'][vQual]
            aQuality = self.config['quality']['audio'][aQual]
            cmd = 'ffmpeg -i "%s" -y %s %s %s %s "%s"' %(inFile, vcodec,vQuality,acodec,aQuality,outFile)
            self.runListeners(cmd)
            print cmd
            try:
                output = self.execute(cmd)
            except ProcessError as e:
                print e.command

    def execute(self,command):
        self.childProcess = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
        logFileName = datetime.datetime.now().strftime('%F_%I%M%S%f').replace('-','')+'.log'
        logFilePath = os.path.join(self.logPath,logFileName)
        outMessage = "Processing..."
        out = ''
        outputBuffer = ''
        while True:
            output = self.childProcess.stderr.read(128)
            outputBuffer = outputBuffer + output
            with open(logFilePath, "a") as logFile:
                logFile.write(output)
            if self.childProcess.poll() != None:
                break
            if outputBuffer.split('\r'):
                out = outputBuffer.split('\r')
                outputBuffer = out.pop(-1)
                if out: outMessage = ' '.join(str(out[-1]).split()).replace('= ','=')
            self.runListeners(outMessage)

    def runListeners(self, info):
        for func in self.listeners:
            func(info)



class PreprocessError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class ProcessError(Exception):
    def __init__(self, command, exitCode, output):
        self.command = command
        self.output = output
        self.exitCode = exitCode
    def __str__(self):
        return repr(self.command,self.output,self.exitCode)
