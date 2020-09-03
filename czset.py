from uipack.czwin import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets,QtGui
import pyqtgraph as pg
from PyQt5.QtCore import *
import os
import subprocess
import glob


class czwin(QtWidgets.QMainWindow,Ui_MainWindow):#残值监视
    sendpath = QtCore.pyqtSignal(str,int,str,str,int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('残差显示')
        self.plotwidget = self.graphicsView
        self.graphicsView.addLegend()
        self.graphicsView.setLabel(axis='left', text='残差')
        self.graphicsView.setLabel(axis='bottom', text='迭代次数')
        self.plotwidget.setBackground('w')
        self.plotwidget.setLimits(xMin=0)
        self.workthread = WorkThread()
        self.startrot = startrot()
        self.init()
        self.connectfrom()
        self.czname = []
        self.data = []
        self.flag = 0
        self.btninner.setText('绘制整体')
        self.setWindowIcon(QtGui.QIcon('./uipack/title.ico'))
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint)


    def timer_start(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.workthread.start)

        self.timer.start(2000)

    def setcheck(self,a,b):
        self.checkBox.setChecked(True)
    def startplot(self):
        self.graphicsView.clear()
        if(self.flag == 0):
            self.flag = 1
        else:
            if (self.checkBox.isChecked()):
                self.graphicsView.plot(self.data[0],self.data[1], pen=pg.mkPen('b', width=3),name=self.czname[1])
            if (self.checkBox_2.isChecked()):
                self.graphicsView.plot(self.data[0],self.data[2], pen=pg.mkPen('y', width=3),name=self.czname[2])
            if (self.checkBox_3.isChecked()):
                self.graphicsView.plot(self.data[0],self.data[3], pen=pg.mkPen('g', width=3),name=self.czname[3])
            if (self.checkBox_4.isChecked()):
                self.graphicsView.plot(self.data[0],self.data[4], pen=pg.mkPen('r', width=3),name=self.czname[4])
            if (self.checkBox_5.isChecked()):
                self.graphicsView.plot(self.data[0],self.data[5], pen=pg.mkPen('c', width=3),name=self.czname[5])
            if (self.checkBox_6.isChecked()):
                self.graphicsView.plot(self.data[0],self.data[6], pen=pg.mkPen('m', width=3),name=self.czname[6])
            if (self.checkBox_7.isChecked()):
                self.graphicsView.plot(self.data[0],self.data[7], pen=pg.mkPen('k', width=3),name=self.czname[7])
            if (self.checkBox_8.isChecked()):
                self.graphicsView.plot(self.data[0],self.data[8], pen=pg.mkPen((255, 0, 255), width=3),name=self.czname[8])
            if (self.checkBox_9.isChecked()):
                self.graphicsView.plot(self.data[0],self.data[9], pen=pg.mkPen((128, 42, 42), width=3),name=self.czname[9])
            if (self.checkBox_10.isChecked()):
                self.graphicsView.plot(self.data[0],self.data[10], pen=pg.mkPen((135, 38, 87), width=3),name=self.czname[10])
            self.flag = 1
    def pri(self):
        pass

    def setui(self,data ,name ):
        self.data = data
        if(self.czname !=name):
            self.czname = name
            if(len(data)-1 >=1):
                self.checkBox.setVisible(True)
                self.checkBox.setText(self.czname[1])
            else:
                self.checkBox.setVisible(False)
            if (len(data)-1 >=2):
                self.checkBox_2.setVisible(True)
                self.checkBox_2.setText(self.czname[2])
            else:
                self.checkBox_2.setVisible(False)
            if (len(data)-1  >= 3):
                self.checkBox_3.setVisible(True)
                self.checkBox_3.setText(self.czname[3])
            else:
                self.checkBox_3.setVisible(False)
            if (len(data)-1  >= 4):
                self.checkBox_4.setVisible(True)
                self.checkBox_4.setText(self.czname[4])
            else:
                self.checkBox_4.setVisible(False)
            if (len(data)-1  >= 5):
                self.checkBox_5.setVisible(True)
                self.checkBox_5.setText(self.czname[5])
            else:
                self.checkBox_5.setVisible(False)
            if (len(data)-1  >= 6):
                self.checkBox_6.setVisible(True)
                self.checkBox_6.setText(self.czname[6])
            else:
                self.checkBox_6.setVisible(False)
            if (len(data)-1  >= 7):
                self.checkBox_7.setVisible(True)
                self.checkBox_7.setText(self.czname[7])
            else:
                self.checkBox_7.setVisible(False)
            if (len(data)-1  >= 8):
                self.checkBox_8.setVisible(True)
                self.checkBox_8.setText(self.czname[8])
            else:
                self.checkBox_8.setVisible(False)
            if (len(data)-1  >= 9):
                self.checkBox_9.setVisible(True)
                self.checkBox_9.setText(self.czname[9])
            else:
                self.checkBox_9.setVisible(False)
            if (len(data)-1  >= 10):
                self.checkBox_10.setVisible(True)
                self.checkBox_10.setText(self.czname[10])
            else:
                self.checkBox.setVisible(False)
        else:
            pass

        '''if(self.flag == 0):
            if (self.checkBox.isVisible()):
                self.graphicsView.plot(pen=pg.mkPen('b', width=3), name=self.czname[1])
            if (self.checkBox_2.isVisible()):
                self.graphicsView.plot(pen=pg.mkPen('y', width=3), name=self.czname[2])
            if (self.checkBox_3.isVisible()):
                self.graphicsView.plot(pen=pg.mkPen('g', width=3), name=self.czname[3])
            if (self.checkBox_4.isVisible()):
                self.graphicsView.plot(pen=pg.mkPen('r', width=3), name=self.czname[4])
            if (self.checkBox_5.isVisible()):
                self.graphicsView.plot(pen=pg.mkPen('c', width=3), name=self.czname[5])
            if (self.checkBox_6.isVisible()):
                self.graphicsView.plot( pen=pg.mkPen('m', width=3), name=self.czname[6])
            if (self.checkBox_7.isVisible()):
                self.graphicsView.plot(pen=pg.mkPen('k', width=3), name=self.czname[7])
            if (self.checkBox_8.isVisible()):
                self.graphicsView.plot( pen=pg.mkPen((255, 0, 255), width=3),name=self.czname[8])
            if (self.checkBox_9.isVisible()):
                self.graphicsView.plot( pen=pg.mkPen((128, 42, 42), width=3),name=self.czname[9])
            if (self.checkBox_10.isVisible()):
                self.graphicsView.plot( pen=pg.mkPen((135, 38, 87), width=3), name=self.czname[10])'''
        self.startplot()

    def connectfrom(self):
        self.checkBox.stateChanged.connect(lambda :self.setui(self.data,self.czname))
        self.checkBox_2.stateChanged.connect(lambda :self.setui(self.data,self.czname))
        self.checkBox_3.stateChanged.connect(lambda :self.setui(self.data,self.czname))
        self.checkBox_4.stateChanged.connect(lambda :self.setui(self.data,self.czname))
        self.checkBox_5.stateChanged.connect(lambda :self.setui(self.data,self.czname))
        self.checkBox_6.stateChanged.connect(lambda :self.setui(self.data,self.czname))
        self.checkBox_7.stateChanged.connect(lambda :self.setui(self.data,self.czname))
        self.checkBox_8.stateChanged.connect(lambda :self.setui(self.data,self.czname))
        self.checkBox_9.stateChanged.connect(lambda :self.setui(self.data,self.czname))
        self.checkBox_10.stateChanged.connect(lambda :self.setui(self.data,self.czname))
        self.workthread.trigger.connect(self.setui)
        self.btnstop.clicked.connect(self.killport)
        self.pushButton.clicked.connect(self.timer_start)
        self.pushButton.clicked.connect(self.startrot.start)
        self.startrot.success.connect(self.success)
        self.startrot.endexe1.connect(self.endexe)



    def endexe(self):
        (QtWidgets.QMessageBox.information(self, '信息提示对话框',
                                           '计算已被终止',
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No))
    def success(self):
        (QtWidgets.QMessageBox.information(self, '信息提示对话框',
                                           '计算已经结束',
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No))
        self.endtime()

    def endtime(self):
        self.timer.stop()
        if(self.startrot.isRunning()):
            self.startrot.quit()


    def init(self):
        self.checkBox.setVisible(False)
        self.checkBox_2.setVisible(False)
        self.checkBox_3.setVisible(False)
        self.checkBox_4.setVisible(False)
        self.checkBox_5.setVisible(False)
        self.checkBox_6.setVisible(False)
        self.checkBox_7.setVisible(False)
        self.checkBox_8.setVisible(False)
        self.checkBox_9.setVisible(False)
        self.checkBox_10.setVisible(False)

    def killport(self):
        self.endtime()
        cmd = 'taskkill /F /IM RotFlow.exe'
        os.system(cmd)

    def selfshow(self,filepath,qunumber,exepath,caseloaction,type):
        self.show()
        self.filepath = filepath
        self.qunumber = qunumber
        self.caseloaction =caseloaction
        self.sendpath.connect(self.workthread.getpath)
        self.sendpath.connect(self.startrot.getpath)
        self.sendpath.emit(self.filepath,self.qunumber,exepath,caseloaction,type)

    def closeEvent(self, event):
        try:
            self.killport()
        except:
            pass





class WorkThread(QThread):
    trigger = QtCore.pyqtSignal(list,list)
    def __int__(self):
        super(WorkThread, self).__init__()
        self.filename = ''
        self.case = ''

    def run(self):
        self.czname = []
        self.data = []
        '''a = glob.glob(self.case + '\RESULT\ResErr.plt')
        if (a == []):
            self.filename = []
        else:
            self.filename = a[0]'''
        if(self.filename !=[]):
            self.readdata(self.filename)
            self.trigger.emit(self.data,self.czname)
        else:
            self.trigger.emit([],[])
    def readdata(self,filename):
        with open(filename, 'r') as file_read:
            while True:
                lines = file_read.readline()
                if not lines:
                    break
                    pass
                if(lines.startswith('VARIABLES')):
                    s = lines.split('VARIABLES="')
                    s = s[1].split('"\n')
                    self.czname = s[0].split('","')
                    for i in range(len(self.czname)):
                        self.data.append([])
                if(lines ==''):
                    pass
                elif(lines.startswith('VARIABLES') == False):
                    for i in range(len(lines.split())):
                        pass
                        self.data[i].append(float(lines.split()[i]))
        file_read.close()

    def getpath(self,path,num,exepath,caselocation,type):


        if(type == 0):
            self.case = caselocation
            a = glob.glob(caselocation+'\RESULT\ResErr.plt')
            if(a == []):
                self.filename = []
            else:
                self.filename = a[0]
        elif(type == 1):
            self.filename = caselocation


class startrot(QThread):
    success = QtCore.pyqtSignal()
    endexe1 = QtCore.pyqtSignal()
    def __int__(self):
        super(startrot, self).__init__()
        self.filename = ''
        self.exelocation = ''


    def run(self):

        self.czname = []
        self.data = []
        filepath = r'cd '+self.filename
        cmd = r'mpiexec -n '+str(self.num) +' '+ self.exelocation
        cmd1 = filepath + '&&' + cmd
        p = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if (p.returncode == 0):
            self.success.emit()
        else:
            self.endexe1.emit()
    def endexe(self,filename):
        with open(filename, 'r') as file_read:
            while True:
                lines = file_read.readline()
                if not lines:
                    break
                    pass
                if(lines.startswith('VARIABLES')):
                    s = lines.split('VARIABLES="')
                    s = s[1].split('"\n')
                    self.czname = s[0].split('","')
                    for i in range(len(self.czname)):
                        self.data.append([])
                if(lines ==''):
                    pass
                elif(lines.startswith('VARIABLES') == False):
                    for i in range(len(lines.split())):
                        pass
                        self.data[i].append(float(lines.split()[i]))
        file_read.close()

    def getpath(self,path,num,exepath,caselocation,type):
        self.filename = path
        self.exelocation =exepath
        self.num = num

















