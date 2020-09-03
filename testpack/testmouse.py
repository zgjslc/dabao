# -*- coding: utf-8 -*-
"""
This example shows how to insert text into a scene using TextItem. This class
is for displaying text that is anchored to a particular location in the data
coordinate system, but which is always displayed unscaled.

For text that scales with the data, use QTextItem.
For text that can be placed in a layout, use LabelItem.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

class MainUi(object):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("州的先生zmister.com A股股票历史走势K线图")
        self.main_widget = QtWidgets.QWidget() # 创建一个主部件
        self.main_layout = QtWidgets.QGridLayout() # 创建一个网格布局
        self.main_widget.setLayout(self.main_layout) # 设置主部件的布局为网格
        self.setCentralWidget(self.main_widget) # 设置窗口默认部件

        self.stock_code = QtWidgets.QLineEdit() # 创建一个文本输入框部件
        self.option_sel = QtWidgets.QComboBox() # 创建一个下拉框部件
        self.option_sel.addItem("近7天")
        self.option_sel.addItem("近30天")
        self.option_sel.addItem("近60天")
        self.option_sel.addItem("近180天")
        self.option_sel.addItem("近360天")
        self.que_btn = QtWidgets.QPushButton("查询") # 创建一个按钮部件
        self.k_widget = QtWidgets.QWidget() # 实例化一个widget部件作为K线图部件
        self.k_layout = QtWidgets.QGridLayout() # 实例化一个网格布局层
        self.k_widget.setLayout(self.k_layout) # 设置K线图部件的布局层
        self.k_plt = pg.PlotWidget() # 实例化一个绘图部件
        self.k_layout.addWidget(self.k_plt) # 添加绘图部件到K线图部件的网格布局层

        # 将上述部件添加到布局层中
        self.main_layout.addWidget(self.stock_code,0,0,1,1)
        self.main_layout.addWidget(self.option_sel,0,1,1,1)
        self.main_layout.addWidget(self.que_btn,0,2,1,1)
        self.main_layout.addWidget(self.k_widget,1,0,3,3)



'''x = np.linspace(-20, 20, 1000)
y = np.sin(x) / x
plot_win = MainUi()

plot = plot_win.k_plt
print(plot)
plot.setYRange(-1, 2)
plot.setWindowTitle('pyqtgraph example: text')
curve = plot.plot(x, y)  ## add a single curve

## Draw an arrowhead next to the text box
arrow = pg.ArrowItem(pos=(0, y.max()), angle=-45)
plot.addItem(arrow)

## Set up an animated arrow and text that track the curve
curvePoint = pg.CurvePoint(curve)
plot.addItem(curvePoint)
text2 = pg.TextItem("test", anchor=(0.5, -1.0))
text2.setParentItem(curvePoint)
arrow2 = pg.ArrowItem(angle=90)
arrow2.setParentItem(curvePoint)

## update position every 10ms
index = 0


def update():
    global curvePoint, index
    index = (index + 1) % len(x)
    curvePoint.setPos(float(index) / (len(x) - 1))
    text2.setText('[%0.1f, %0.1f]' % (x[index], y[index]))


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()'''

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = plot_win()
    mainWindow.show()
    sys.exit(app.exec_())