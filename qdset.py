from uipack.qdwin import Ui_Dialog
from PyQt5 import QtCore, QtWidgets,QtGui
import pyqtgraph as pg
from PyQt5.QtCore import *
import os
import glob


class qdwin(QtWidgets.QDialog,Ui_Dialog):#残值监视
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('气动力矩')
        self.plotwidget = self.graphicsView
        self.graphicsView.addLegend()
        self.labelplot = pg.TextItem()
        self.plotwidget.setBackground('w')


        self.filepath =''
        self.filelist = []
        self.namelist = []
        self.data = []
        self.datalist = []
        self.setWindowIcon(QtGui.QIcon('./uipack/title.ico'))
        self.connectfrom()
        self.proxy = pg.SignalProxy(self.graphicsView.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

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



    def mouseMoved(self,evt):


        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.graphicsView.sceneBoundingRect().contains(pos):
            mousePoint = self.graphicsView.plotItem.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            pos_y = int(mousePoint.y())
            print(index)


            '''if 0 < index < len(data.index):
                print(xdict[index], data['open'][index], data['close'][index])
                self.labelplot.setHtml(
                    "<p style='color:white'>日期：{0}</p><p style='color:white'>开盘：{1}</p><p style='color:white'>收盘：{2}</p>".format(
                        xdict[index], data['open'][index], data['close'][index]))'''
            self.labelplot.setPos(mousePoint.x(), mousePoint.y())
            self.vLine.setPos(mousePoint.x())
            #self.hLine.setPos(mousePoint.y())


    def readdate(self):
        self.datalist = []
        for i in range(len(self.filelist)):
            filename = self.filelist[i]
            with open(filename,'r') as file:
                self.data = []
                while True:
                    lines = file.readline()
                    if not lines:
                        self.datalist.append(self.data)
                        break
                        pass
                    if(lines.startswith('VARIABLES')):
                        s = lines.split('VARIABLES="')
                        s = s[1].split('"\n')
                        self.namelist = s[0].split('","')
                        for index in self.namelist:
                            self.data.append([])
                    elif(lines == ''):
                        pass
                    else:
                        s = lines.split()
                        for j in range(len(s)):
                            self.data[j].append(float(s[j]))
        self.qdcomx1.clear()
        self.qdcomy1.clear()
        for i in self.namelist:
            self.qdcomx1.addItem(i)
            self.qdcomy1.addItem(i)

    def plotwin(self):
        self.graphicsView.clear()
        self.graphicsView.setLabel(axis='left', text=self.qdcomy1.currentText())
        self.graphicsView.setLabel(axis='bottom', text=self.qdcomx1.currentText())
        if (self.checkBox_2.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_2.currentIndex()][self.qdcomx1.currentIndex()], self.datalist[self.qdcom1_2.currentIndex()][self.qdcomy1.currentIndex()],
                               pen=pg.mkPen('b', width=3),name = self.qdcom1_2.currentText()+'——'+self.qdcomx1.currentText()+'——'+self.qdcomy1.currentText())
        if (self.checkBox_3.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_3.currentIndex()][self.qdcomx1.currentIndex()], self.datalist[self.qdcom1_3.currentIndex()][self.qdcomy1.currentIndex()],
                               pen=pg.mkPen('y', width=3),name = self.qdcom1_3.currentText()+'——'+self.qdcomx1.currentText()+'——'+self.qdcomy1.currentText())
        if (self.checkBox_4.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_4.currentIndex()][self.qdcomx1.currentIndex()], self.datalist[self.qdcom1_4.currentIndex()][self.qdcomy1.currentIndex()],
                               pen=pg.mkPen('g', width=3),name = self.qdcom1_4.currentText()+'——'+self.qdcomx1.currentText()+'——'+self.qdcomy1.currentText())
        if (self.checkBox_5.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_5.currentIndex()][self.qdcomx1.currentIndex()], self.datalist[self.qdcom1_5.currentIndex()][self.qdcomy1.currentIndex()],
                               pen=pg.mkPen('r', width=3),name = self.qdcom1_5.currentText()+'——'+self.qdcomx1.currentText()+'——'+self.qdcomy1.currentText())
        if (self.checkBox_6.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_6.currentIndex()][self.qdcomx1.currentIndex()], self.datalist[self.qdcom1_6.currentIndex()][self.qdcomy1.currentIndex()],
                               pen=pg.mkPen('c', width=3),name = self.qdcom1_6.currentText()+'——'+self.qdcomx1.currentText()+'——'+self.qdcomy1.currentText())
        if (self.checkBox_7.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_7.currentIndex()][self.qdcomx1.currentIndex()], self.datalist[self.qdcom1_7.currentIndex()][self.qdcomy1.currentIndex()],
                               pen=pg.mkPen('m', width=3),name = self.qdcom1_7.currentText()+'——'+self.qdcomx1.currentText()+'——'+self.qdcomy1.currentText())
        if (self.checkBox_8.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_8.currentIndex()][self.qdcomx1.currentIndex()], self.datalist[self.qdcom1_8.currentIndex()][self.qdcomy1.currentIndex()],
                               pen=pg.mkPen('k', width=3),name = self.qdcom1_8.currentText()+'——'+self.qdcomx1.currentText()+'——'+self.qdcomy1.currentText())
        if (self.checkBox_9.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_9.currentIndex()][self.qdcomx1.currentIndex()], self.datalist[self.qdcom1_9.currentIndex()][self.qdcomy1.currentIndex()],
                               pen=pg.mkPen((255, 0, 255), width=3),name = self.qdcom1_9.currentText()+'——'+self.qdcomx1.currentText()+'——'+self.qdcomy1.currentText())
        if (self.checkBox_10.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_10.currentIndex()][self.qdcomx1.currentIndex()], self.datalist[self.qdcom1_10.currentIndex()][self.qdcomy1.currentIndex()],
                               pen=pg.mkPen((128, 42, 42), width=3),name = self.qdcom1_10.currentText()+'——'+self.qdcomx1.currentText()+'——'+self.qdcomy1.currentText())
        if (self.checkBox_11.isChecked()):
            self.graphicsView.plot(self.datalist[self.qdcom1_11.currentIndex()][self.qdcomx1.currentIndex()], self.datalist[self.qdcom1_11.currentIndex()][self.qdcomy1.currentIndex()],
                               pen=pg.mkPen((135, 38, 87), width=3),name = self.qdcom1_11.currentText()+'——'+self.qdcomx1.currentText()+'——'+self.qdcomy1.currentText())
        pass

    def setui(self):
        if(len(self.filelist)>=1):
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
    def selfshow(self,filepath):
        self.vLine = pg.InfiniteLine(angle=90, movable=True)  # 创建一个垂直线条
        self.hLine = pg.InfiniteLine(angle=0, movable=True)  # 创建一个水平线条
        self.graphicsView.addItem(self.vLine, ignoreBounds=True)  # 在图形部件中添加垂直线条
        self.graphicsView.addItem(self.hLine, ignoreBounds=True)  # 在图形部件中添加水平线条
        self.vLine.setPos(0.4289130034945741)
        self.filepath =  filepath
        a = filepath
        try:
            self.filelist = []
            if(a !=[]):
                for file in a:
                    self.filelist.append(file)
                self.setui()
                self.readdate()
                self.plotwin()
                self.setcheck()
                self.show()

            else:
                pass
                self.show()
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
