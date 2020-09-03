from testpack.testmouse import MainUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
import sys
import numpy as np
import pyqtgraph as pg
class plot_win(QtWidgets.QMainWindow,MainUi):
    def __init__(self):
        super().__init__()
        self.x = np.linspace(-20, 20, 1000)
        self.y = np.sin(self.x) / self.x
        self.k_plt.setYRange(-1, 2)
        curve = self.k_plt.plot(self.x, self.y)
        arrow = pg.ArrowItem(pos=(0, self.y.max()), angle=-45)
        self.k_plt.addItem(arrow)
        self.curvePoint = pg.CurvePoint(curve)
        self.k_plt.addItem(self.curvePoint)
        self.text2 = pg.TextItem("test", anchor=(0.5, -1.0))
        self.text2.setParentItem(self.curvePoint)
        arrow2 = pg.ArrowItem(angle=90)
        arrow2.setParentItem(self.curvePoint)
        self.move_slot = pg.SignalProxy(self.k_plt.scene().sigMouseMoved, rateLimit=60, slot=self.print_slot)
        self.index = 0
        #self.timeset()

    def timeset(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

    def update(self):
        self.index = (self.index + 1) % len(self.x)
        ax = float(self.index) / (len(self.x) - 1)
        self.curvePoint.setPos(ax)
        self.text2.setText('[%0.1f, %0.1f]' % (self.x[self.index], self.y[self.index]))

    def find_nearest(self,array, value):
        idx = (np.abs(array - value)).argmin()
        return array[idx],idx

    def print_slot(self, event=None):
        if event is None:
            print("事件为空")
        else:
            pos = event[0]  # 获取事件的鼠标位置
            if self.k_plt.sceneBoundingRect().contains(pos):
                mousePoint = self.k_plt.plotItem.vb.mapSceneToView(pos)  # 转换鼠标坐标
                index = float(mousePoint.x())  # 鼠标所处的X轴坐标
                pos_y = float(mousePoint.y())  # 鼠标所处的Y轴坐标
                self.x1 = np.array(self.x)
                index , idx = self.find_nearest(self.x1, index)
                pos_bili = (index - self.x[0]) / (self.x[-1] - self.x[0])

                if( abs(self.y[idx] - pos_y) <=0.1):
                    self.curvePoint.setPos(pos_bili)
                    self.text2.setText('[%0.1f, %0.1f]' % (self.x[idx], self.y[idx]))




if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = plot_win()
    mainWindow.show()
    sys.exit(app.exec_())