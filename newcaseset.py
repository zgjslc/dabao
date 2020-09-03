from uipack.newcase import Ui_Dialog
from PyQt5 import QtCore, QtWidgets,QtGui
import os
import shutil
class newcase(QtWidgets.QDialog,Ui_Dialog):
    sendpath = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('新建项目')
        self.cwd = os.getcwd()
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QtGui.QIcon('./uipack/title.ico'))
        self.lineEdit.setText(self.cwd)
        self.btnfilepath.clicked.connect(self.setfilepath)
        self.btnmeshpath.clicked.connect(self.setmeshpath)
        self.btnok.clicked.connect(self.okclick)
        self.btncancel.clicked.connect(self.close)
        self.filepath = ''
        self.meshpath = []
        self.filemesh = ''
        self.lineEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit_3.setFocusPolicy(QtCore.Qt.NoFocus)
        with open('exepath.txt','r') as file:
                filepath = file.readline()

        file.close()
        filepath = self.getpath(filepath)
        self.lineEdit.setText(filepath)



    def getpath(self,filepath):
        s = filepath.split('/')
        s = filepath.split('/'+s[-1])
        return s[0]

    def setfilepath(self):

        with open('exepath.txt','r') as file:
                self.filepath = file.readline()
        file.close()
        self.filepath = self.getpath(self.filepath)
        fileName, ok2 = QtWidgets.QFileDialog.getSaveFileName(self,
                                                              "新建项目",
                                                              self.filepath)
        if(fileName !=''):
            self.filemesh = fileName
            self.lineEdit.setText(fileName)
        pass

    def setmeshpath(self):
        with open('exepath.txt','r') as file:
                self.filepath = file.readline().split()[0]
        file.close()
        self.filepath = self.getpath(self.filepath)
        meshpath, type = QtGui.QFileDialog.getOpenFileNames(None, "请选择要添加的文件", self.filepath,
                                                           "All Files (*);;Exe Files (*.exe)")
        if(meshpath !=[]):
            self.meshpath = meshpath
            s = self.meshpath[0].split('/')
            s = self.meshpath[0].split('/'+s[-1])
            self.lineEdit_3.setText(s[0])
            self.meshfileoath = s[0]
        pass

    def okclick(self):

        if(os.path.exists(self.filemesh)):
            (QtWidgets.QMessageBox.information(self, '信息提示对话框',
                                               '已存在该项目',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No))
            return 0
        elif(self.filemesh == '' or self.meshpath == []):
            (QtWidgets.QMessageBox.information(self, '信息提示对话框',
                                               '请完成设置',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No))
            return 0

        else:
            filemesh = self.filemesh.split()[0]+ '/MESH'
            fileresult = self.filemesh.split()[0] + '/RESULT'
            shutil.copytree(self.meshfileoath, filemesh)
            os.makedirs(fileresult)
            self.sendpath.emit(self.filemesh.split()[0])
            self.close()

        pass