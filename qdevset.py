from uipack.qdevwin import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets,QtGui
from scipy.optimize import leastsq
from scipy.fftpack import fft
from scipy.integrate import odeint
import numpy as np
import pyqtgraph as pg
import matplotlib.pyplot as plt
from math import sin,acos,cos
from PyQt5.QtCore import *
import os
import glob


#class qdevwin(QtWidgets.QMainWindow, Ui_MainWindow):
class qdevwin():
    def __init__(self):
        super().__init__()

        self.iter = []
        self.time = []
        self.fx = []
        self.fy = []
        self.fz = []
        self.mx = []
        self.my = []
        self.mz = []
        self.namelist = []
        self.datalist = []
        '''self.setupUi(self)
        self.setWindowTitle('气动分布评估')
        self.plotwidget = self.graphicsView
        self.graphicsView.addLegend()
        self.plotwidget.setBackground('w')
        self.setWindowIcon(QtGui.QIcon('./uipack/title.ico'))
        self.connectfrom()'''

    def addfile(self):
        filepath = self.filelist[0]
        qdFilepath, type = QtGui.QFileDialog.getOpenFileNames(None, "请选择文件", filepath,
                                                              "Exe Files (*.plt);;All Files (*)")
        if (qdFilepath != []):
            for file in qdFilepath:
                if file not in self.filelist:
                    self.filelist.append(file)
        else:
            pass
        self.setui()
        self.datalist = []

        for file in self.filelist:
            self.readfile(file)
        self.qdcomx1.clear()
        self.qdcomy1.clear()
        for i in self.namelist:
            self.qdcomx1.addItem(i)
            self.qdcomy1.addItem(i)
        self.plotwin()
        self.setcheck()
        self.show()

    def connectfrom(self):
        self.qdcomx1.currentIndexChanged.connect(self.plotwin)
        self.qdcomy1.currentIndexChanged.connect(self.plotwin)
        self.qdcom1_2.currentIndexChanged.connect(self.plotwin)
        self.qdcom1_3.currentIndexChanged.connect(self.plotwin)
        self.qdcom1_4.currentIndexChanged.connect(self.plotwin)
        self.qdcom1_5.currentIndexChanged.connect(self.plotwin)
        self.qdcom1_6.currentIndexChanged.connect(self.plotwin)
        self.qdcom1_7.currentIndexChanged.connect(self.plotwin)
        self.qdcom1_8.currentIndexChanged.connect(self.plotwin)
        self.qdcom1_9.currentIndexChanged.connect(self.plotwin)
        self.qdcom1_10.currentIndexChanged.connect(self.plotwin)
        self.qdcom1_11.currentIndexChanged.connect(self.plotwin)
        self.checkBox_2.stateChanged.connect(self.plotwin)
        self.checkBox_3.stateChanged.connect(self.plotwin)
        self.checkBox_4.stateChanged.connect(self.plotwin)
        self.checkBox_5.stateChanged.connect(self.plotwin)
        self.checkBox_6.stateChanged.connect(self.plotwin)
        self.checkBox_7.stateChanged.connect(self.plotwin)
        self.checkBox_8.stateChanged.connect(self.plotwin)
        self.checkBox_9.stateChanged.connect(self.plotwin)
        self.checkBox_10.stateChanged.connect(self.plotwin)
        self.checkBox_11.stateChanged.connect(self.plotwin)
        self.actionfile.triggered.connect(self.addfile)

    def getgunzhaun(self,a,b):
        self. CNA = a / b
        pass

    def readfile(self,filename):


        if filename != '':
            self.iter = []
            self.time = []
            self.fx = []
            self.fy = []
            self.fz = []
            self.mx = []
            self.my = []
            self.mz = []
            self.data = []
            with open(filename,'r') as file:


                while True:
                    lines = file.readline()
                    if not lines:
                        self.datalist.append(self.data)
                        break
                        pass
                    else:
                        if (lines.startswith('VARIABLES')):
                            s = lines.split('VARIABLES="')
                            s = s[1].split('"\n')
                            a = s[0].split('","')

                            if(len(a) <= len(self.namelist)):
                                self.namelist = s[0].split('","')
                            elif(self.namelist == []):
                                self.namelist = s[0].split('","')
                            else:
                                pass

                            for index in a:
                                self.data.append([])
                        elif (lines == ''):
                            pass
                        else:
                            s = lines.split()
                            for j in range(len(s)):
                                self.data[j].append(float(s[j]))



    def FUN_one(self,p,x):
        a1, a2 = p
        return a1*x+a2


    def error_one(self,p,x,y):
        return self.FUN_one(p,x)-y


    def FUN_two(self,p,x):
        a1, a2, a3 = p
        return a1*x**2+a2*x+a3


    def error_two(self,p,x,y):
        return self.FUN_two(p,x) - y


    def least_square(self,p,x,y):
        if(len(p) == 2):
            para = leastsq(self.error_one,p,args=(x,y))
        elif(len(p) == 3):
            para = leastsq(self.error_two, p, args=(x, y))
        else:
            return 0
        return para

    def average(self,x,y):
        a = np.true_divide(y,x)
        return np.mean(a)

    def FFT(self,fs,data):
        L = len(data)
        N = np.power(2, np.ceil(np.log2(L)))
        N = int(N)
        FFT_y1 = np.abs(fft(data, N)) / L * 2  # 振幅大小
        fre = np.arange(int(N / 2)) * fs / N * 2#获取频率

        FFT_y1 = FFT_y1[range(int(N / 2))]
        a = sorted(FFT_y1)
        return a[-3], a[-2], a[-1],fre, FFT_y1

    def plotwin(self,x,y):
        a = pg.plot(x,y, pen=pg.mkPen('b', width=3),name = 'firstcase')

        pass

    def selfshow(self,filepath):
        self.filepath =  filepath
        a = filepath
        try:
            self.filelist = []
            if(a !=[]):
                for file in a:
                    self.filelist.append(file)
                self.setui()
                self.datalist = []

                for file in self.filelist:

                    self.readfile(file)
                self.qdcomx1.clear()
                self.qdcomy1.clear()
                for i in self.namelist:
                    self.qdcomx1.addItem(i)
                    self.qdcomy1.addItem(i)
                self.plotwin()
                self.setcheck()
                self.show()

            else:
                pass
        except:
            pass


    def setcheck(self):
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)
        self.checkBox_6.setChecked(False)
        self.checkBox_7.setChecked(False)
        self.checkBox_8.setChecked(False)
        self.checkBox_9.setChecked(False)
        self.checkBox_10.setChecked(False)
        self.checkBox_11.setChecked(False)


    def additem(self,com):
        com.clear()
        self.itemlist = []
        for file in self.filelist:
            a = file.split('/')
            a = a[-1].split('.plt')
            self.itemlist.append(a[0])
        for item in self.itemlist:
            com.addItem(item)

    def plotwin(self):
        self.graphicsView.clear()
        self.graphicsView.setLabel(axis='left', text=self.qdcomy1.currentText())
        self.graphicsView.setLabel(axis='bottom', text=self.qdcomx1.currentText())
        if (self.checkBox_2.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_2.currentIndex()][self.qdcomx1.currentIndex()],
                                   self.datalist[self.qdcom1_2.currentIndex()][self.qdcomy1.currentIndex()],
                                   pen=pg.mkPen('b', width=3),
                                   name=self.qdcom1_2.currentText() + '——' + self.qdcomx1.currentText() + '——' + self.qdcomy1.currentText())
        if (self.checkBox_3.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_3.currentIndex()][self.qdcomx1.currentIndex()],
                                   self.datalist[self.qdcom1_3.currentIndex()][self.qdcomy1.currentIndex()],
                                   pen=pg.mkPen('y', width=3),
                                   name=self.qdcom1_3.currentText() + '——' + self.qdcomx1.currentText() + '——' + self.qdcomy1.currentText())
        if (self.checkBox_4.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_4.currentIndex()][self.qdcomx1.currentIndex()],
                                   self.datalist[self.qdcom1_4.currentIndex()][self.qdcomy1.currentIndex()],
                                   pen=pg.mkPen('g', width=3),
                                   name=self.qdcom1_4.currentText() + '——' + self.qdcomx1.currentText() + '——' + self.qdcomy1.currentText())
        if (self.checkBox_5.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_5.currentIndex()][self.qdcomx1.currentIndex()],
                                   self.datalist[self.qdcom1_5.currentIndex()][self.qdcomy1.currentIndex()],
                                   pen=pg.mkPen('r', width=3),
                                   name=self.qdcom1_5.currentText() + '——' + self.qdcomx1.currentText() + '——' + self.qdcomy1.currentText())
        if (self.checkBox_6.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_6.currentIndex()][self.qdcomx1.currentIndex()],
                                   self.datalist[self.qdcom1_6.currentIndex()][self.qdcomy1.currentIndex()],
                                   pen=pg.mkPen('c', width=3),
                                   name=self.qdcom1_6.currentText() + '——' + self.qdcomx1.currentText() + '——' + self.qdcomy1.currentText())
        if (self.checkBox_7.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_7.currentIndex()][self.qdcomx1.currentIndex()],
                                   self.datalist[self.qdcom1_7.currentIndex()][self.qdcomy1.currentIndex()],
                                   pen=pg.mkPen('m', width=3),
                                   name=self.qdcom1_7.currentText() + '——' + self.qdcomx1.currentText() + '——' + self.qdcomy1.currentText())
        if (self.checkBox_8.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_8.currentIndex()][self.qdcomx1.currentIndex()],
                                   self.datalist[self.qdcom1_8.currentIndex()][self.qdcomy1.currentIndex()],
                                   pen=pg.mkPen('k', width=3),
                                   name=self.qdcom1_8.currentText() + '——' + self.qdcomx1.currentText() + '——' + self.qdcomy1.currentText())
        if (self.checkBox_9.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_9.currentIndex()][self.qdcomx1.currentIndex()],
                                   self.datalist[self.qdcom1_9.currentIndex()][self.qdcomy1.currentIndex()],
                                   pen=pg.mkPen((255, 0, 255), width=3),
                                   name=self.qdcom1_9.currentText() + '——' + self.qdcomx1.currentText() + '——' + self.qdcomy1.currentText())
        if (self.checkBox_10.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_10.currentIndex()][self.qdcomx1.currentIndex()],
                                   self.datalist[self.qdcom1_10.currentIndex()][self.qdcomy1.currentIndex()],
                                   pen=pg.mkPen((128, 42, 42), width=3),
                                   name=self.qdcom1_10.currentText() + '——' + self.qdcomx1.currentText() + '——' + self.qdcomy1.currentText())
        if (self.checkBox_11.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_11.currentIndex()][self.qdcomx1.currentIndex()],
                                   self.datalist[self.qdcom1_11.currentIndex()][self.qdcomy1.currentIndex()],
                                   pen=pg.mkPen((135, 38, 87), width=3),
                                   name=self.qdcom1_11.currentText() + '——' + self.qdcomx1.currentText() + '——' + self.qdcomy1.currentText())
        pass




    def setui(self):
        if (len(self.filelist) >= 1):
            self.checkBox_2.setVisible(True)
            self.label_4.setVisible(True)
            self.qdcom1_2.setVisible(True)
            self.additem(self.qdcom1_2)
        else:
            self.checkBox_2.setVisible(False)
            self.label_4.setVisible(False)
            self.qdcom1_2.setVisible(False)
        if (len(self.filelist) >= 2):
            self.checkBox_3.setVisible(True)
            self.label_5.setVisible(True)
            self.qdcom1_3.setVisible(True)
            self.additem(self.qdcom1_3)
        else:
            self.checkBox_3.setVisible(False)
            self.label_5.setVisible(False)
            self.qdcom1_3.setVisible(False)
        if (len(self.filelist) >= 3):
            self.checkBox_4.setVisible(True)
            self.label_6.setVisible(True)
            self.qdcom1_4.setVisible(True)
            self.additem(self.qdcom1_4)
        else:
            self.checkBox_4.setVisible(False)
            self.label_6.setVisible(False)
            self.qdcom1_4.setVisible(False)
        if (len(self.filelist) >= 4):
            self.checkBox_5.setVisible(True)
            self.label_7.setVisible(True)
            self.qdcom1_5.setVisible(True)
            self.additem(self.qdcom1_5)
        else:
            self.checkBox_5.setVisible(False)
            self.label_7.setVisible(False)
            self.qdcom1_5.setVisible(False)
        if (len(self.filelist) >= 5):
            self.checkBox_6.setVisible(True)
            self.label_8.setVisible(True)
            self.qdcom1_6.setVisible(True)
            self.additem(self.qdcom1_6)
        else:
            self.checkBox_6.setVisible(False)
            self.label_8.setVisible(False)
            self.qdcom1_6.setVisible(False)
        if (len(self.filelist) >= 6):
            self.checkBox_7.setVisible(True)
            self.label_9.setVisible(True)
            self.qdcom1_7.setVisible(True)
            self.additem(self.qdcom1_7)
        else:
            self.checkBox_7.setVisible(False)
            self.label_9.setVisible(False)
            self.qdcom1_7.setVisible(False)
        if (len(self.filelist) >= 7):
            self.checkBox_8.setVisible(True)
            self.label_10.setVisible(True)
            self.qdcom1_8.setVisible(True)
            self.additem(self.qdcom1_8)
        else:
            self.checkBox_8.setVisible(False)
            self.label_10.setVisible(False)
            self.qdcom1_8.setVisible(False)
        if (len(self.filelist) >= 8):
            self.checkBox_9.setVisible(True)
            self.label_11.setVisible(True)
            self.qdcom1_9.setVisible(True)
            self.additem(self.qdcom1_9)
        else:
            self.checkBox_9.setVisible(False)
            self.label_11.setVisible(False)
            self.qdcom1_9.setVisible(False)
        if (len(self.filelist) >= 9):
            self.checkBox_10.setVisible(True)
            self.label_12.setVisible(True)
            self.qdcom1_10.setVisible(True)
            self.additem(self.qdcom1_10)
        else:
            self.checkBox_10.setVisible(False)
            self.label_12.setVisible(False)
            self.qdcom1_10.setVisible(False)
        if (len(self.filelist) >= 10):
            self.checkBox_11.setVisible(True)
            self.label_13.setVisible(True)
            self.qdcom1_11.setVisible(True)
            self.additem(self.qdcom1_11)
        else:
            self.checkBox_11.setVisible(False)
            self.label_13.setVisible(False)
            self.qdcom1_11.setVisible(False)
        pass

class odeslover:
    def __init__(self):
        self.param = {'a1':0,'a2':0,'a3':0,'b10':0,'b11':0,'b20':0,'b21':0,'b3':0,'b40':0,'b41':0,
                      'b42':0,'b50':0,'b51':0,'b52':0,'c1':0,'c2':0,'c3':0,'FN':0,'FZ':0,'MZ':0,'MY':0,'dz1':0.,
                      'dy1':0.,'dx':0.,'Ix':0.,'It':0.,'wx':0.}

        pass


    def setinitparam(self):

        pass


    def refreshparam(self):
        pass


    def readdata(self):
        with open (self.filename,'r') as file:
            while True:
                lines = file.readline()
                if not lines:
                    break
                    pass
                else:
                    pass


    def savefile(self,filepath):
        with open (filepath,'w+') as file:
            pass


    def runge_kutta(self, y, x, dx, f):

        """ y is the initial value for y
               x is the initial value for x
               dx is the time step in x
               f is derivative of function y(t)
           """

        k1 = dx * f(y, x)
        k2 = dx * f(y + 0.5 * k1, x + 0.5 * dx)
        k3 = dx * f(y + 0.5 * k2, x + 0.5 * dx)
        k4 = dx * f(y + k3, x + dx)
        return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6.


    def FUNCASE_1(self, y, t):
        if(len(y) == 4):
            a,b,q,r = y
            return np.array([self.FUN_a(a,b,q,r),self.FUN_b(a,b,q,r),self.FUN_q(a,b,q,r),self.FUN_r(a,b,q,r)])
        elif(len(y) == 5):
            a,b,q,r,wx = y
            return np.array([self.FUN_a(a,b,q,r),self.FUN_b(a,b,q,r),self.FUN_qtwo(a,b,q,r,wx),self.FUN_qtwo(a,b,q,r,wx),self.FUN_wx(wx),self.FUN_rtwo(wx,b,r)])

    def FUN_a(self,a,b,q,r):#a的微分方程
        return (r + r*a**2 + r*b**2 + q*a*b - (self.param['a1'] + self.param['FN'])*a - (self.param['a2']
                +self.param['FZ'])*b - self.param['a3']*self.param['dz1'])


    def FUN_b(self,a,b,q,r):#b的微分方程
        return q + q*b**2 - (self.param['a1']+self.param['FN'])*b + (self.param['a2'] + self.param['FZ'])*a - self.param['a3']*self.param['dy1']


    def FUN_q(self,a,b,q,r):#q的微分方程
        return ( -(self.param['Ix']/self.param['It'])*self.param['wx']*r - r**2*b + (self.param['b10']+self.param['b11']*acos(cos(a)*cos(b))+self.param['MZ'])
                *b + (self.param['b20']+self.param['b21'] * acos(cos(a)*cos(b))+self.param['MY'])* a + self.param['b3']*self.param['dy1'] +
                (self.param['b40']+self.param['b41']*acos(cos(a)*cos(b)) + self.param['b42']*(acos(cos(a)*cos(b)))**2)*q + (self.param['b50']+self.param['b51']*acos(cos(a)*cos(b))
                +self.param['b52']*acos(cos(a)*cos(b))**2)*r)


    def FUN_r(self,a,b,q,r):
        return ( (self.param['Ix']/self.param['It']*self.param['wx']*q) + (q*r*b) + (self.param['b10']*self.param['b11']*acos(cos(a)*cos(b))+self.param['MZ'])*a
                - (self.param['b20']+self.param['b21']*acos(cos(a)*cos(b)) + self.param['MY'])*b +
                self.param['b3']*self.param['dz1'] + (self.param['b40']+self.param['b41']*acos(cos(a)*cos(b))+self.param['b42']*(acos(cos(a)*cos(b)))**2)*r -
                (self.param['b50']+self.param['b51']*acos(cos(a)*cos(b))+self.param['b52']*acos(cos(a)*cos(b))**2)*q )


    def FUN_wx(self,wx):
        return self.param['c1'] +self.param['c2']*wx +self.param['c3']*self.param['dx']


    def FUN_rtwo(self,wx,b,r):
        return wx - r * b


    def FUN_qtwo(self,a,b,q,r,wx):
        return (-(self.param['Ix'] / self.param['It']) * wx * r - r ** 2 * b + (
                    self.param['b10'] + self.param['b11'] * acos(cos(a) * cos(b)) + self.param['MZ'])
                * b + (self.param['b20'] + self.param['b21'] * acos(cos(a) * cos(b)) + self.param['MY']) * a +
                self.param['b3'] * self.param['dy1'] +
                (self.param['b40'] + self.param['b41'] * acos(cos(a) * cos(b)) + self.param['b42'] * acos(
                    cos(a) * cos(b)) ** 2) * q + (self.param['b50'] + self.param['b51'] * acos(cos(a) * cos(b))
                                                  + self.param['b52'] * acos(cos(a) * cos(b)) ** 2) * r)
    def FUN_rsec(self,a,b,q,r,wx):
        return ((self.param['Ix'] / self.param['It'] * wx * q) + (q * r * b) + (
                    self.param['b10'] * self.param['b11'] * acos(cos(a) * cos(b)) + self.param['MZ']) * a
                - (self.param['b20'] + self.param['b21'] * acos(cos(a) * cos(b)) + self.param['MY']) * b +
                self.param['b3'] * self.param['dz1'] + (
                            self.param['b40'] + self.param['b41'] * acos(cos(a) * cos(b)) + self.param['b42'] * acos(
                        cos(a) * cos(b)) ** 2) * r -
                (self.param['b50'] + self.param['b51'] * acos(cos(a) * cos(b)) + self.param['b52'] * acos(
                    cos(a) * cos(b)) ** 2) * q)


if __name__ == "__main__":
    qd = qdevwin()
    a = np.array([0,2,4,6,8,10,12,15,20,25])
    cna = np.array([0,0.0243,0.0255,0.0294,0.0335,0.0356,0.0421,0.0540,0.0382,0.0298])
    plt.figure()
    plt.plot(a)
    plt.show()


