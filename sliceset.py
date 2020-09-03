from uipack.slicewin import Ui_Dialog
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtCore import *
class slicewin(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QtGui.QIcon('./uipack/title.ico'))
        regx = QRegExp("[-+]?\d{,3}[.]?\d{,3}[ ][-+]?\d{,3}[.]?\d{,3}[ ][-+]?\d{,3}[.]?\d{,3}")
        validator = QtGui.QRegExpValidator(regx, self.textpoint)
        self.textpoint.setValidator(validator)
        regx = QRegExp("[-+]?\d{,3}[.]?\d{,3}[ ][-+]?\d{,3}[.]?\d{,3}[ ][-+]?\d{,3}[.]?\d{,3}")
        validator = QtGui.QRegExpValidator(regx, self.textnormal)
        self.textnormal.setValidator(validator)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint)



