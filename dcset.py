from uipack.dcwin import Ui_Dialog
from PyQt5 import QtCore, QtWidgets,QtGui
class dcwin(QtWidgets.QDialog,Ui_Dialog):#定常计算
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textout.setValidator(QtGui.QIntValidator(1, 65535))
        self.textinner.setValidator(QtGui.QIntValidator(1, 65535))
        self.textinone.setValidator(QtGui.QIntValidator(1, 65535))
        self.textcancha.setValidator(QtGui.QIntValidator(-65532, 0))
        self.textnt.setValidator(QtGui.QIntValidator(1, 65535))
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint|QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QtGui.QIcon('./uipack/title.ico'))

