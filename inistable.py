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
from qdevset import odeslover
class inistable:
    def __init__(self):
        self.a_max = 10.
        self.num = 10.
        self.da = 2*self.a_max/self.num
        self.data_a = []
        self.data_b = []
        self.slover = odeslover()
        self.time = np.linspace(0,10,100)

        pass


    def set_mesh(self,amax,bmax,num):#设置数据网格
        self.data_a = []
        self.data_b = []
        for i in range(num+1):
            self.data_a.append(round(i * 2*amax/num - amax,4))
            self.data_b.append(round(i * 2*bmax/num - bmax,4))
        return self.data_a,self.data_b

        pass


    def testdata(self,a,b): #判断是否满足初值约束
        if(acos(cos(a)*cos(b)) <= self.a_max):
            return True
        elif(acos(cos(a)*cos(b)) > self.a_max):
            return False

    def testwending(self,a,b,t): #求解微分方程并返回结果
        if(self.testdata(a,b)):
            for key in self.slover.param:
                self.slover.param[key] = 1

            trick = odeint(self.slover.FUNCASE_1,y0=[a,b,0,0],t=t)
            return trick


if __name__== '__main__':
    ini = inistable()

    trick = ini.testwending(2,0,ini.time))

