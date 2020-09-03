from uipack.duopian import Ui_Dialog as dpwin
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtCore import *
class dpwin(QtWidgets.QDialog,dpwin):#舵偏界面
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint|QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.width(), self.height())
        self.com.currentIndexChanged.connect(self.dptype)#切换界面
        self.btncancel.clicked.connect(self.close)#关闭界面
        self.labelbalance.setText('平衡位置(\260)')
        self.labelzhengfu.setText('振幅(\260)')
        self.labelpinglv.setText('频率(Hz)')
        self.labelxiangwei.setText('初始相位(\260)')
        self.textbalance.setToolTip('输入平衡位置')
        self.textzhengfu.setToolTip('输入振幅大小')
        self.textpinlv.setToolTip('输入频率大小')
        self.textbalance.setValidator(QtGui.QDoubleValidator(-65535, 65535, 2))
        self.textpinlv.setValidator(QtGui.QDoubleValidator(-65535, 65535, 2))
        self.textxiangwei.setValidator(QtGui.QDoubleValidator(-65535, 65535, 2))
        self.textzhengfu.setValidator(QtGui.QDoubleValidator(-65535, 65535, 2))
        regx = QRegExp("[-+]?\d{,3}[.]?\d{,3}[ ][-+]?\d{,3}[.]?\d{,3}[ ][-+]?\d{,3}[.]?\d{,3}")
        validator = QtGui.QRegExpValidator(regx, self.textcent)
        self.textcent.setValidator(validator)
        validator = QtGui.QRegExpValidator(regx, self.textaxis)
        self.textaxis.setValidator(validator)
        regx = QRegExp("(\d{,3}\d{,3}[ ]\d{,3}\d{,3}[ ]\d{,3}\d{,3})+")
        validator = QtGui.QRegExpValidator(regx, self.textzone)
        self.textzone.setValidator(validator)



        self.setWindowIcon(QtGui.QIcon('./uipack/title.ico'))

    def dptype(self):#切换界面
        if(self.com.currentIndex()==0):
            self.labelbalance.setText('平衡位置(\260)')
            self.textbalance.setToolTip('输入平衡位置')
            self.textzhengfu.setToolTip('输入振幅大小')
            self.textpinlv.setToolTip('输入频率大小')
            self.labelzhengfu.setText('振幅(\260)')
            self.labelpinglv.setText('频率(Hz)')
            self.labelxiangwei.setText('初始相位(\260)')
            self.labelxiangwei.setVisible(True)
            self.textxiangwei.setVisible(True)
            self.dpclear()

        else:
            self.labelbalance.setText('角位置')
            self.labelzhengfu.setText('角速度')
            self.labelpinglv.setText('角加速度')
            self.textbalance.setToolTip('输入角位置所在列数')
            self.textzhengfu.setToolTip('输入角速度所在列数')
            self.textpinlv.setToolTip('输入角加速度所在列数')
            self.labelxiangwei.setVisible(False)
            self.textxiangwei.setVisible(False)
            self.dpclear()
    def dpclear(self):#清除数据
        self.textbalance.clear()
        self.textzhengfu.clear()
        self.textxiangwei.clear()
        self.textpinlv.clear()
