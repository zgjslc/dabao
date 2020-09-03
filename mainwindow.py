from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from uipack.mainwin import Ui_MainWindow
from dcset import dcwin
from dpset import dpwin
from czset import czwin
from newcaseset import newcase
from sliceset import slicewin
import readcfg as readfile
import glob
import os
import mesh_build as mb
import innermesh as ib
import pyvista as pv
import meshslice as ms
from qdset import qdwin
import numpy as np
from qdevset import qdevwin


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    clickSignal = QtCore.pyqtSignal(str,int,str,str,int)
    meshignal = QtCore.pyqtSignal(list,str)
    meshbegin = QtCore.pyqtSignal()
    sbsignal = QtCore.pyqtSignal()
    qdsignal = QtCore.pyqtSignal(list)
    qdevsignal = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.addplotter()
        self.readdata = readdata()
        self.Initialization()
        self.dpwin = dpwin()
        self.dcwin = dcwin()
        self.czwin = czwin()
        self.qdwin = qdwin()
        self.qdevwin = qdevwin()
        self.slicewin = slicewin()
        self.newcase = newcase()
        self.connectform()
        self.mb = mb.buildmesh()
        self.ib = ib.buildmesh()
        self.Meshslice = ms.buildmesh()
        self.plottype = 0
        self.setrange()
        self.savefilename = ' '
        self.actionsave.setText('保存图片')
        self.actionsaveas.setText('图片另存为')
        self.setWindowTitle("非定常计算仿真软件")
        self.setWindowIcon(QtGui.QIcon('./uipack/title.ico'))
        self.tabWidget.setCurrentIndex(0)




    def setexepath(self):
        exepath,type =  QtGui.QFileDialog.getOpenFileNames(None, "请选择求解器", self.exepath, "Exe Files (*.exe);;All Files (*)")
        if(exepath !=[]):
            if(exepath[0] != ''):
                self.exepath = exepath[0]
                self.yx_exepath.setText(self.exepath.split()[0])
                with open('exepath.txt','w') as file:
                    file.write(self.caselocation+'\n')
                    file.write(self.exepath + '\n')
                file.close()

    def canchabiao(self):#显示残值表
        czFilepath, type = QtGui.QFileDialog.getOpenFileName(None, "请选择残值文件", self.caselocation,
                                                           "Exe Files (*.plt);;All Files (*)")

        if(czFilepath!=''):
            s = self.wg_qunum_2.text().split()
            qunumber = 0
            for i in s:
                qunumber = int(i) + qunumber
            s = self.caselocation.split('/')
            s = self.caselocation.split('/' + s[-1])
            self.caselocation = czFilepath
            self.clickSignal.emit(s[0],int(qunumber),self.yx_exepath.text(),self.caselocation,1)
            self.czwin.graphicsView.clear()
            self.czwin.workthread.start()
        else:
            pass


    def addplotter(self):
        pass

    def locationcheck(self):#检查是否已经选择项目
        if(len(glob.glob(self.caselocation + '\\*.cfg2')) ==0):
            (QtWidgets.QMessageBox.information(self, '信息提示对话框',
                                                 '请先设置参数文件',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No))
            return False
        else:
            return True
    #界面初始化
    def Initialization(self):
        self.btnchooseexe.setText('选择求解器')
        self.hy_comnum.setCurrentIndex(5)
        self.gz_radwhole.setChecked(True)
        self.fy_plv.setText('俯仰频率（Hz)')
        self.fy_balance.setText('平衡位置(\260)')
        self.fy_xiangwei.setText('初始相位(\260)')
        self.fy_zhenfu.setText('俯仰振幅(\260)')
        self.label_llma.setText('来流马赫数(Ma)')
        self.label_llleinuochangdu.setText('雷诺数参考长度(m)')
        self.label_qdcd.setText('气动力矩参考长度(m)')
        self.label_qdmj.setText('气动力参考面积(m^2)')
        self.label_qdzx.setText('气动力矩参考中心(X,Y,Z)')
        self.label_llyingjaio.setText('来流迎角(\260)')
        self.label_chooseexe.setText('求解器选择')
        self.ld_comldtype.setCurrentIndex(0)
        self.ld_comtltype.setVisible(False)
        self.label_ldtltype.setVisible(False)
        self.ld_comsimtype.setCurrentIndex(1)
        self.dp_com.setCurrentIndex(4)
        self.dpcent = [0]*4
        self.dpaxis = [0]*4
        self.dplaw = [0]*4
        self.dpzone = [0]*4
        self.dpyz = [3]*4
        self.dpflag = [1,2,3,4]
        self.caselocation = 'C:'
        self.gridlist = []
        self.grid = pv.UnstructuredGrid()
        self.hy_comnum.setCurrentIndex(0)
        self.choosehynum()
        self.gz_zone.setVisible(False)
        self.label_gzzone.setVisible(False)
        self.label_qjcfl3.setVisible(False)
        self.qj_textcfl3.setVisible(False)
        self.exepath = ''
        self.zhentifilename = []
        with open('exepath.txt','r') as file:
                self.caselocation = file.readline()
                self.exepath = file.readline()
        file.close()
        self.meshlist = []
        self.zhenntimeshlist = []
        self.sliceflag = False
        self.slicemeshlist =[]
        self.zhenticomname = []
        self.wg_painyi.setText('0.0 0.0 0.0')
        self.btn_refresh.setVisible(False)
        pass

    #建立槽函数
    def connectform(self):
        self.wg_btnchosecase.clicked.connect(self.choosecase)

        self.hy_comnum.currentIndexChanged.connect(self.choosehynum)
        self.fy_comtype.currentIndexChanged.connect(self.fytype)
        self.ld_comsimtype.currentIndexChanged.connect(self.fdctype)
        self.ld_comldtype.currentIndexChanged.connect(self.ldtype)
        self.dp_com.currentIndexChanged.connect(self.dpnum)
        self.dp_btnset1.clicked.connect(lambda :self.opendp(self.dpflag[0]))
        self.dp_btnset2.clicked.connect(lambda: self.opendp(self.dpflag[1]))
        self.dp_btnset3.clicked.connect(lambda: self.opendp(self.dpflag[2]))
        self.dp_btnset4.clicked.connect(lambda: self.opendp(self.dpflag[3]))
        self.dpwin.btnok.clicked.connect(lambda: self.closedp(self.dpflag[ self.dpcon- 5]))
        self.dpwin.btncancel.clicked.connect(self.dpwin.close)
        self.ld_btnset.clicked.connect(self.opendcwin)
        self.ld_btnset.clicked.connect(self.dcwin.show)
        self.qj_comtuijin.currentIndexChanged.connect(self.cflset)
        self.gz_radwhole.toggled.connect(self.opengz)
        self.btnstart.clicked.connect(self.savecfg)
        self.dcwin.btnok.clicked.connect(self.dcwin.close)
        self.dcwin.btncancel.clicked.connect(self.dcwin.close)
        self.pushstartmesh.clicked.connect(self.sendemit)
        self.clickSignal.connect(self.czwin.selfshow)
        self.actionbianjie.triggered.connect(self.plotmesh)
        self.meshignal.connect(self.readdata.getpath)
        self.meshbegin.connect(self.readdata.start)
        self.actioninnner.triggered.connect(self.plottt)
        self.sbsignal.connect(lambda:self.plottt())
        self.readdata.datasignal.connect(lambda: self.fillplotter(self.offset, self.cells, self.celltype, self.points, self.name, self.property,
                                          self.data))
        self.czwin.btnbianjie.clicked.connect(self.czbianjie)
        self.czwin.btninner.clicked.connect(self.czinner)
        self.actionslice.triggered.connect(self.slicewinshow)
        self.slicewin.btnok.clicked.connect(self.meshslice)
        self.slicewin.btncancel.clicked.connect(self.slicewin.close)
        self.actioncancha.triggered.connect(self.canchabiao)
        self.actionsave.triggered.connect(self.savepng)
        self.actionsaveas.triggered.connect(self.savepngas)
        self.btnchooseexe.clicked.connect(self.setexepath)
        self.actionnew.triggered.connect(self.newcase.show)
        self.newcase.sendpath.connect(self.setcurrentcase)
        self.btn_refresh.clicked.connect(self.movescene)
        self.checkmesh.stateChanged.connect(self.refreshplotter)
        self.checkoutline.stateChanged.connect(self.refreshplotter)
        self.combar.currentIndexChanged.connect(self.refreshplotter)
        self.actionqidong.triggered.connect(self.qdshow)
        self.qdsignal.connect(self.qdwin.selfshow)
        self.btn_top.clicked.connect(lambda :self.movescene('top'))
        self.btn_bottom.clicked.connect(lambda: self.movescene('bottom'))
        self.btn_front.clicked.connect(lambda: self.movescene('front'))
        self.btn_back.clicked.connect(lambda: self.movescene('back'))
        self.btn_left.clicked.connect(lambda: self.movescene('left'))
        self.btn_right.clicked.connect(lambda: self.movescene('right'))
        self.actionqdpinggu.triggered.connect(self.qdevshow)
        self.qdevsignal.connect(self.qdevwin.selfshow)
        pass


    def movescene(self,type):
        focal_pt = self.plotter.center
        if(type == 'top'):
            cpos = ((0, 0, 1) + np.array(focal_pt),
                    focal_pt, (0, 1, 0))
        elif(type == 'bottom'):
            cpos = ((0, 0, -1) + np.array(focal_pt),
                    focal_pt, (0, 1, 0))
        elif(type == 'front'):
            cpos = ((0, 1, 0) + np.array(focal_pt),
                    focal_pt, (0, 0, 1))
        elif(type == 'back'):
            cpos = ((0, -1, 0) + np.array(focal_pt),
                    focal_pt, (0, 0, 1))
        elif (type == 'left'):
            cpos = ((1, 0, 0) + np.array(focal_pt),
                    focal_pt, (0, 0, 1))
        elif (type == 'right'):
            cpos = ((-1, 0, 0) + np.array(focal_pt),
                    focal_pt, (0, 0, 1))
        else:
            return 0
        self.plotter.camera_position = cpos
        self.plotter.reset_camera()
        if(self.zhenntimeshlist !=[]):
            self.plotter.camera.Zoom(3)
        pass

    def qdshow(self):
        filepath = self.caselocation + '/RESULT'
        qdFilepath, type = QtGui.QFileDialog.getOpenFileNames(None, "请选择文件", filepath,
                                                           "Exe Files (*.plt);;All Files (*)")
        if(qdFilepath !=[]):
            self.qdsignal.emit(qdFilepath)
        else:
            pass
        pass

    def qdevshow(self):
        filepath = self.caselocation
        qdFilepath, type = QtGui.QFileDialog.getOpenFileNames(None, "请选择文件", filepath,
                                                           "Exe Files (*.plt);;All Files (*)")
        if(qdFilepath !=[]):
            self.qdevsignal.emit(qdFilepath)
        else:
            pass
        pass

    def refreshplotter(self):#刷新界面
        if(self.combar.count() != 0):
            if(self.sliceflag ):
                if(self.slicemeshlist !=[] and self.zhenntimeshlist !=[]):
                    self.sliceplotter()
                pass
            else:
                if(self.meshlist != [] ):
                    self.bianjieplotter()
                elif(self.zhenntimeshlist !=[]):
                    self.zhentiplotter()
        else:
            pass

    def getexepath(self):
        pass

    def savepngas(self):#图片另存为
        fileName, ok2 = QtWidgets.QFileDialog.getSaveFileName(self,
                                                              "文件保存",
                                                              "C:/",
                                                              "Png Files (*.png)")

        if(fileName != ''):
            self.savefilename = fileName
            self.plotter.screenshot(self.savefilename)
        else:
            pass

    def savepng(self):#保存图片
        if(self.savefilename == ' '):
            fileName, ok2 = QtWidgets.QFileDialog.getSaveFileName(self,
                                                         "文件保存",
                                                         "C:/",
                                                         "Png Files (*.png)")

            if (fileName != ''):
                self.savefilename = fileName
                self.plotter.screenshot(self.savefilename)
            else:
                pass
        else:
            self.plotter.screenshot(self.savefilename)


    def slicewinshow(self):#显示切面选择界面
        if (self.locationcheck()):
            if(self.zhenntimeshlist ==[]):
                a = self.readzhentifile()
                if(a ==0):
                    return 0
                elif(a ==1):
                    pass
            else:
                pass
            self.slicewin.show()
        else:
            pass


    def meshslice(self):#切片功能
        try:
            self.sliceflag = True
            self.slicewin.close()
            cent = self.slicewin.textpoint.text()
            normal1 = self.slicewin.textnormal.text()
            b = str(cent.split())
            b = b.replace("'", '')
            b = b.replace("'", '')
            a = list(eval(b))
            point = tuple(a)
            b = str(normal1.split())
            b = b.replace("'", '')
            b = b.replace("'", '')
            a = list(eval(b))
            normal = tuple(a)

            filename = self.zhentifilename
            for i in range(len(filename)):
                if ('Rsu' in filename[i]):
                    grid, name = self.Meshslice.meshplot(filename[i])
                    slice = grid.slice(normal=normal, origin=point)
                    if (slice.n_points > 0):
                        self.slicemeshlist.append(slice)
            self.sliceplotter()

        except:
            self.sendmessege('切片参数')

    def sliceplotter(self):
        self.zhentiplotter()
        self.plotter.camera_set = True
        for index in self.slicemeshlist:
            self.plotter.add_mesh(index, show_edges=False,
                                      scalars=self.zhenticomname[self.combar.currentIndex()])
    def readzhentifile(self):
        try:
            if (self.locationcheck()):
                filepath = self.caselocation + '/RESULT'
                filename, type = QtGui.QFileDialog.getOpenFileNames(None, "请选择文件", filepath,
                                                                   "Plt Files (*.plt);;All Files (*)")

                if(filename != []):
                    self.zhentifilename = filename
                    self.zhenntimeshlist = []
                    self.meshlist = []
                    self.meshinnercomfill('Rsu')
                    for i in range(len(filename)):

                        if ('Rsu' in filename[i]):
                            grid, self.zhentiname, type = self.ib.meshplot(filename[i])
                            if (type == 1):
                                self.zhenticomname = self.zhentiname
                                self.zhenntimeshlist.append(grid)
                    return 1
                else:
                    return 0
        except:
            self.sendmessege('结果文件')

    def plottt(self):#读取整体
        try:
           self.sliceflag = False
           self.readzhentifile()
           self.zhentiplotter()
           self.plotter.reset_camera()
           self.plotter.camera.Zoom(3)
        except:
            self.sendmessege('结果文件')

    def zhentiplotter(self):#绘制整体


        cpos = self.plotter.camera_position
        self.plotter.clear()

        for index in self.zhenntimeshlist:
            if (self.checkmesh.isChecked()):
                self.plotter.add_mesh(index, show_edges=True,
                                      scalars=self.zhenticomname[self.combar.currentIndex()])
            else:
                self.plotter.add_mesh(index, show_edges=False,
                                      scalars=self.zhenticomname[self.combar.currentIndex()])
            if (self.checkoutline.isChecked()):
                self.plotter.add_mesh(index.outline())
        self.plotter.camera_position = cpos

        #self.plotter.reset_camera()
        self.plotter.show_axes()


    def setcurrentcase(self,filepath):#设置当前项目
        self.plotter.clear()
        self.caselocation = filepath
        self.filename = self.caselocation.split('/')
        self.parent_path = os.path.dirname(self.caselocation)
        self.setcurrent(self.filename[-1])
        self.fillwg()
        self.hycomset()
        self.cfglocation = len(glob.glob(self.caselocation + '\\parms.cfg2'))
        if (self.cfglocation == 1):
            self.readfile(glob.glob(self.caselocation + '\\parms.cfg2')[0])
        else:
            self.readfile('')
            pass


    def choosecase(self):
        #补上一个默认文件路径
        with open('exepath.txt','r') as file:
                line = file.readline()
                self.exepath = file.readline()
        file.close()
        loaction = self.caselocation
        self.caselocation = QtWidgets.QFileDialog.getExistingDirectory(self,'选择项目网格',line)
        if(self.caselocation == 'C:'):
            return 0
        elif(self.caselocation !=''):
            if(len(glob.glob(self.caselocation + '\\mesh\\*.inp'))==0):
                (QtWidgets.QMessageBox.information(self, '信息提示对话框',
                '该文件夹中无网格文件',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No))
            else:
                self.zhenntimeshlist = []
                self.setcurrentcase(self.caselocation)
        elif(self.caselocation == ''):
            self.caselocation = loaction
            return 0

    def readmesh(self,file_name='nmd'):  # 获得网格文件位置
        self.plotmesh(file_name)

    def readfile(self,filename):#读取cfg文件
        self.combar.clear()
        try:
            self.NMSH, self.MTYP, self.NMRK, self.NPRT, self.TRNS, self.NCSY, self.ROTX, self.ROTYZTYPE, self.ROTYZ, \
            self.NROT, self.DPCENT, self.DPAXIS, self.DPLAW, self.DPZONE, self.NSLD, self.HYLD, self.NSTP, self.DELT, self.LDTYPE, \
            self.TLTYPE, self.XUSUAN, self.LLMA, self.LLYJ, self.LLLNS, self.LLCKCD, self.QDCD, self.QDMJ, self.QDZX, self.QDZBX, \
            self.QJDL, self.QJTJ, self.QJCFL, self.QJCFL3, self.LDSIMTYPE, self.JSOUT, self.JSINNER, self.JSINONE, self.JSCANZHI, \
            self.YXCANZHI, self.JSNT, self.YXJIEGUO, self.YXXUSUAN, self.GZZONE = readfile.readcfg().readfile(filename)
            self.loadfile()


        except:
            self.sendmessege('参数文件')

    #修改current.dat
    def setcurrent(self,casename):#设置dat文件
        filepath = self.parent_path + '/current.dat'
        xieru = open(filepath, 'w')
        xieru.write('$Project')
        str = '\nProjName            =  "' + casename +'"'
        xieru.write(str)
        xieru.write('\n/')
        xieru.close()

    #读取mesh文件夹
    def fillwg(self):#填充网格数据
        wgqunum =0
        qunumlist = []
        Meshunum = 0
        Meshnumlist = []
        self.qunum = glob.glob(self.caselocation + '\\mesh\\*.inp')
        if(len(self.qunum) ==0):
            (QtWidgets.QMessageBox.information(self, '信息提示对话框',
                                               '该文件夹中无网格文件',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No))
            return 0
        else:
            pass
        self.wg_btnchosecase.setText(self.filename[-1])

        for inp in self.qunum:
            s = inp.split('mesh\\')
            if(s[1][0].isdigit()):
                qunumlist.append(inp)
                wgqunum = wgqunum+1
        self.qunum = qunumlist

        meshnum = glob.glob(self.caselocation+'\\mesh\\*.vrt')
        for vrt in meshnum:
            s = vrt.split('mesh\\')
            if(s[1][0].isdigit()):
                Meshnumlist.append(vrt)
                Meshunum = Meshunum+1




        self.wg_qunum.setText(str(wgqunum))
        bjtype = []
        wgnum = []
        for i in range(wgqunum):
            bianjienum = 0
            with open(qunumlist[i], 'r') as file_read:
                while True:
                    lines = file_read.readline()
                    if not lines:
                        break
                        pass
                    if lines.startswith('RDEF'):
                        bianjienum = bianjienum+1
                        pass
            bjtype.append(str(bianjienum)+' ')
        s = ''.join(bjtype)
        self.wg_bianjienum.setText(s)
        for i in range(Meshunum):
            meshhe = 0
            with open(Meshnumlist[i],'r') as file_read:
                while True:
                    lines = file_read.readline()
                    if not lines:
                        break
                        pass
                    else:
                        meshhe = meshhe+1
                        pass
            wgnum.append(str(meshhe)+' ')
        s= ''.join(wgnum)
        self.wg_qunum_2.setToolTip(s)
        self.yx_exepath.setText(self.exepath.split()[0])
        with open('exepath.txt','w') as file:
                file.write(self.caselocation)
                file.write('\n')
                file.write(self.exepath + '\n')
        file.close()


    #滑移运动combox设置
    def hycomset(self):
        self.hy_lcom1.clear()
        self.hy_lcom2.clear()
        self.hy_lcom3.clear()
        self.hy_lcom4.clear()
        self.hy_lcom5.clear()
        self.hy_rcom1.clear()
        self.hy_rcom2.clear()
        self.hy_rcom3.clear()
        self.hy_rcom4.clear()
        self.hy_rcom5.clear()

        for i in range(len(self.qunum)):
            self.hy_lcom1.addItem(str(i+1))
            self.hy_lcom2.addItem(str(i+1))
            self.hy_lcom3.addItem(str(i+1))
            self.hy_lcom4.addItem(str(i+1))
            self.hy_lcom5.addItem(str(i+1))
            self.hy_rcom1.addItem(str(i+1))
            self.hy_rcom2.addItem(str(i+1))
            self.hy_rcom3.addItem(str(i+1))
            self.hy_rcom4.addItem(str(i+1))
            self.hy_rcom5.addItem(str(i+1))

        pass
    #滑移数量设置
    def choosehynum(self):
        s = self.hy_comnum.currentIndex()
        if(s==0):
            self.hy1('noshow')
            self.hy2('noshow')
            self.hy3('noshow')
            self.hy4('noshow')
            self.hy5('noshow')
        elif(s==1):
            self.hy1('show')
            self.hy2('noshow')
            self.hy3('noshow')
            self.hy4('noshow')
            self.hy5('noshow')
        elif (s == 2):
            self.hy1('show')
            self.hy2('show')
            self.hy3('noshow')
            self.hy4('noshow')
            self.hy5('noshow')
        elif (s == 3):
            self.hy1('show')
            self.hy2('show')
            self.hy3('show')
            self.hy4('noshow')
            self.hy5('noshow')
        elif (s == 4):
            self.hy1('show')
            self.hy2('show')
            self.hy3('show')
            self.hy4('show')
            self.hy5('noshow')
        elif (s == 5):
            self.hy1('show')
            self.hy2('show')
            self.hy3('show')
            self.hy4('show')
            self.hy5('show')

        pass

    #滑移边界显示
    def hy1(self,state='show'):
        if(state=='show'):
            self.hy_lab1.setVisible(True)
            self.hy_lcom1.setVisible(True)
            self.hy_ltext1.setVisible(True)
            self.hy_rcom1.setVisible(True)
            self.hy_rtext1.setVisible(True)
        elif(state=='noshow'):
            self.hy_lab1.setVisible(False)
            self.hy_lcom1.setVisible(False)
            self.hy_ltext1.setVisible(False)
            self.hy_rcom1.setVisible(False)
            self.hy_rtext1.setVisible(False)
    def hy2(self,state='show'):
        if (state == 'show'):
            self.hy_lab2.setVisible(True)
            self.hy_lcom2.setVisible(True)
            self.hy_ltext2.setVisible(True)
            self.hy_rcom2.setVisible(True)
            self.hy_rtext2.setVisible(True)
        elif (state == 'noshow'):
            self.hy_lab2.setVisible(False)
            self.hy_lcom2.setVisible(False)
            self.hy_ltext2.setVisible(False)
            self.hy_rcom2.setVisible(False)
            self.hy_rtext2.setVisible(False)
    def hy3(self,state='show'):
        if (state == 'show'):
            self.hy_lab3.setVisible(True)
            self.hy_lcom3.setVisible(True)
            self.hy_ltext3.setVisible(True)
            self.hy_rcom3.setVisible(True)
            self.hy_rtext3.setVisible(True)
        elif (state == 'noshow'):
            self.hy_lab3.setVisible(False)
            self.hy_lcom3.setVisible(False)
            self.hy_ltext3.setVisible(False)
            self.hy_rcom3.setVisible(False)
            self.hy_rtext3.setVisible(False)
    def hy4(self,state='show'):
        if (state == 'show'):
            self.hy_lab4.setVisible(True)
            self.hy_lcom4.setVisible(True)
            self.hy_ltext4.setVisible(True)
            self.hy_rcom4.setVisible(True)
            self.hy_rtext4.setVisible(True)
        elif (state == 'noshow'):
            self.hy_lab4.setVisible(False)
            self.hy_lcom4.setVisible(False)
            self.hy_ltext4.setVisible(False)
            self.hy_rcom4.setVisible(False)
            self.hy_rtext4.setVisible(False)
    def hy5(self,state='show'):
        if (state == 'show'):
            self.hy_lab5.setVisible(True)
            self.hy_lcom5.setVisible(True)
            self.hy_ltext5.setVisible(True)
            self.hy_rcom5.setVisible(True)
            self.hy_rtext5.setVisible(True)
        elif (state == 'noshow'):
            self.hy_lab5.setVisible(False)
            self.hy_lcom5.setVisible(False)
            self.hy_ltext5.setVisible(False)
            self.hy_rcom5.setVisible(False)
            self.hy_rtext5.setVisible(False)

    #滚转运动设置
    def opengz(self):
        if(self.gz_radwhole.isChecked()):
            self.label_gzzone.setVisible(False)
            self.gz_zone.setVisible(False)
        else:
            if(int(self.wg_qunum.text().strip()) ==1):
                self.gz_radwhole.setChecked(True)
                (QtWidgets.QMessageBox.information(self, '信息提示对话框', '网格区过少，无法进行局部滚转',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No))

            else:
                self.label_gzzone.setVisible(True)
                self.gz_zone.setVisible(True)
        pass

    #俯仰运动开启
    def openfy(self):
        if(self.fy_radio.isChecked()):
            self.groupBox_15.setEnabled(False)
        pass
    #俯仰运动切换
    def fytype(self):
        if(self.fy_comtype.currentIndex()==0):
            self.wg_painyi.setVisible(True)
            self.label_wgpy.setVisible(True)
            self.groupBox_16.setVisible(True)
            self.fy_comaxis.setVisible(True)
            self.label_fyaxis.setVisible(True)
        elif(self.fy_comtype.currentIndex()==1):
            self.groupBox_16.setVisible(False)
            self.fy_comaxis.setVisible(False)
            self.label_fyaxis.setVisible(False)
            self.wg_painyi.setVisible(False)
            self.label_wgpy.setVisible(False)
            pass

    #舵偏运动切换
    def dpnum(self):
        if(self.dp_com.currentIndex() == 0):
            self.dp1('noshow')
            self.dp2('noshow')
            self.dp3('noshow')
            self.dp4('noshow')
        elif (self.dp_com.currentIndex() == 1):
            self.dp1('show')
            self.dp2('noshow')
            self.dp3('noshow')
            self.dp4('noshow')
        elif (self.dp_com.currentIndex() == 2):
            self.dp1('show')
            self.dp2('show')
            self.dp3('noshow')
            self.dp4('noshow')
        elif (self.dp_com.currentIndex() == 3):
            self.dp1('show')
            self.dp2('show')
            self.dp3('show')
            self.dp4('noshow')
        elif (self.dp_com.currentIndex() == 4):
            self.dp1('show')
            self.dp2('show')
            self.dp3('show')
            self.dp4('show')
        pass
    def dp1(self,state='show'):
        if(state=='show'):
            self.dp_lab1.setVisible(True)
            self.dp_btnset1.setVisible(True)
        elif(state=='noshow'):
            self.dp_btnset1.setVisible(False)
            self.dp_lab1.setVisible(False)
            pass
    def dp2(self,state='show'):
        if(state=='show'):
            self.dp_lab2.setVisible(True)
            self.dp_btnset2.setVisible(True)
        elif(state=='noshow'):
            self.dp_btnset2.setVisible(False)
            self.dp_lab2.setVisible(False)
            pass
    def dp3(self,state='show'):
        if(state=='show'):
            self.dp_lab3.setVisible(True)
            self.dp_btnset3.setVisible(True)
        elif(state=='noshow'):
            self.dp_btnset3.setVisible(False)
            self.dp_lab3.setVisible(False)
            pass
    def dp4(self,state='show'):
        if(state=='show'):
            self.dp_lab4.setVisible(True)
            self.dp_btnset4.setVisible(True)
        elif(state=='noshow'):
            self.dp_btnset4.setVisible(False)
            self.dp_lab4.setVisible(False)
            pass

    #打开舵偏界面
    def opendp(self,flag):
        self.dpcon = flag
        if(flag <=4):
            self.dpwin.setWindowTitle('舵偏运动' + str(flag))
            self.dpwin.dpclear()
            self.dpwin.textcent.clear()
            self.dpwin.textaxis.clear()
            self.dpwin.textzone.clear()
        else:

            self.dpwin.setWindowTitle('舵偏运动' + str(flag - 4))
            self.dpwin.textcent.setText(str(self.dpcent[flag - 5]))
            self.dpwin.textaxis.setText(str(self.dpaxis[flag - 5]))
            dplist = str(self.dplaw[flag - 5]).split(' ')
            if(dplist[0] == '2'):
                self.dpwin.com.setCurrentIndex(0)
                self.dpwin.dptype()
                self.dpwin.textbalance.setText(str(dplist[1]))
                self.dpwin.textzhengfu.setText(str(dplist[2]))
                self.dpwin.textpinlv.setText(str(dplist[3]))
                self.dpwin.textxiangwei.setText(str(dplist[4]))
                self.dpwin.textzone.setText(str(self.dpzone[flag - 5]))
            elif(dplist[0] == '4'):
                self.dpwin.com.setCurrentIndex(1)
                self.dpwin.dptype()
                self.dpwin.textbalance.setText(str(dplist[1]))
                self.dpwin.textzhengfu.setText(str(dplist[2]))
                self.dpwin.textpinlv.setText(str(dplist[3]))
                self.dpwin.textzone.setText(str(self.dpzone[flag - 5]))

        self.dpwin.show()
        if(flag <= 4 ):
            self.dpflag[flag - 1] = flag+4



        pass
    def closedp(self,flag):

        self.dpcent[flag-5] = self.dpwin.textcent.text()
        self.dpaxis[flag-5] = self.dpwin.textaxis.text()
        self.dpzone[flag-5] = self.dpwin.textzone.text()
        if(self.dpwin.com.currentIndex()==0):

            law = '2 '
            law = law + self.dpwin.textbalance.text() + ' '
            law = law + self.dpwin.textzhengfu.text() + ' '
            law = law + self.dpwin.textpinlv.text() + ' '
            law = law + self.dpwin.textxiangwei.text()
            self.dplaw[flag-5] = law


            #self.dpyz[flag-5] = self.dpwin.comYZ.currentIndex()
        elif(self.dpwin.com.currentIndex()==1):
            law = '4 '
            law = law + self.dpwin.textbalance.text() + ' '
            law = law + self.dpwin.textzhengfu.text() + ' '
            law = law + self.dpwin.textpinlv.text() + ' '
            self.dplaw[flag - 5] = law
        self.dpwin.close()
        pass

    #非定常运动切换
    def fdctype(self):
        if(self.ld_comsimtype.currentIndex()==0):
            if(self.fy_comtype.currentIndex()==1 and self.dp_com.currentIndex()==0):
                self.ld_btnset.setText('定常计算设置')
                self.dcwin.setWindowTitle('定常计算设置')
            else:
                (QtWidgets.QMessageBox.information(self, '信息提示对话框',
                                                   '含有舵偏运动或俯仰运动，无法进行定常计算', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No))
                self.ld_comsimtype.setCurrentIndex(1)
        elif(self.ld_comsimtype.currentIndex()==1):
            self.ld_btnset.setText('非定常计算设置')
            self.dcwin.setWindowTitle('非定常计算设置')

        pass

    ##非定常计算界面设置
    def opendcwin(self):
        if(self.ld_comsimtype.currentText() == '定常计算'):
            self.dcwin.labelouter.setVisible(False)
            self.dcwin.labelinone.setVisible(False)
            self.dcwin.labelnt.setVisible(False)
            self.dcwin.labeltime.setVisible(False)
            self.dcwin.texttime.setVisible(False)
            self.dcwin.textout.setVisible(False)
            self.dcwin.textinone.setVisible(False)
            self.dcwin.textnt.setVisible(False)
            self.dcwin.labelinner.setText('迭代步数')
        elif(self.ld_comsimtype.currentText() == '非定常计算'):
            self.dcwin.labelouter.setVisible(True)
            self.dcwin.labelinone.setVisible(True)
            self.dcwin.labelnt.setVisible(True)
            self.dcwin.labeltime.setVisible(True)
            self.dcwin.textinone.setVisible(True)
            self.dcwin.textout.setVisible(True)
            self.dcwin.texttime.setVisible(True)
            self.dcwin.textnt.setVisible(True)
            self.dcwin.labelinner.setText('虚拟时间步数')



        pass

    #流动类型切换
    def ldtype(self):
        if (self.ld_comldtype.currentIndex()==0 or self.ld_comldtype.currentIndex()==1):
            self.ld_comtltype.setVisible(False)
            self.label_ldtltype.setVisible(False)
        elif(self.ld_comldtype.currentIndex()==2):
            self.ld_comtltype.setVisible(True)
            self.label_ldtltype.setVisible(True)
        pass

    #CFL值设置
    def cflset(self):
        if(self.qj_comtuijin.currentIndex() == 0):
            self.label_qjcfl.setVisible(True)
            self.qj_textcfl.setVisible(True)
            self.label_qjcfl3.setVisible(False)
            self.qj_textcfl3.setVisible(False)
        elif(self.qj_comtuijin.currentIndex() == 1):
            pass
        pass

    #参数设置
    def loadfile(self):
        a = ' '

        if(self.NPRT !=a):#分区数量设置
            self.wg_qunum_2.setText(self.NPRT)
        else:
            self.wg_qunum_2.clear()

        if(self.NSLD!=a):#滑移面设置
            self.hy_comnum.setCurrentIndex(int(self.NSLD))
            self.leftlist = []
            self.leftinlist = []
            self.rightlist = []
            self.rightinlist = []
            for i in range(int(self.NSLD)):
                left, leftin,right,rightin = self.hysplit(self.HYLD[i])
                self.leftlist.append(left)
                self.leftinlist.append(leftin)
                self.rightlist.append(right)
                self.rightinlist.append(rightin)
            self.hyfill()
        else:
            self.hy_comnum.setCurrentIndex(0)


        if(str(self.NCSY) == '1'):#滚转俯仰运动设置
            self.gz_radwhole.setChecked(True)
            self.gz_law.setText(self.ROTX[0][2:])
        elif(str(self.NCSY) == '2'):
            self.gz_radpart.setChecked(True)
            self.gz_law.setText(self.ROTX[0][2:])
            self.gz_zone.setText(self.GZZONE[0][2:])
        else:
            self.gz_radwhole.setChecked(True)
            self.gz_law.clear()
            self.gz_zone.clear()

        if(self.ROTYZTYPE == 'Y' or self.ROTYZTYPE == 'Z'):
            self.fy_comtype.setCurrentIndex(0)
            self.wg_painyi.setVisible(True)
            self.label_wgpy.setVisible(True)
            self.wg_painyi.setText(self.TRNS)
            if(self.ROTYZTYPE == 'Y'):
                self.fy_comaxis.setCurrentIndex(0)
            else:
                self.fy_comaxis.setCurrentIndex(1)
            if(self.ROTYZ.startswith('2 ')):
                s = self.ROTYZ.split()
                self.fy_textbalance.setText(s[1])
                self.fy_textzhenfu.setText(s[2])
                self.fy_textplv.setText(s[3])
                self.fy_textxiangwei.setText(s[4])
        else:
            self.wg_painyi.setVisible(False)
            self.label_wgpy.setVisible(False)
            self.fy_comtype.setCurrentIndex(1)

        if (str(self.NROT) != a):#舵偏运动
            self.dp_com.setCurrentIndex(int(self.NROT))
            for i in range(int(self.NROT)):
                self.dpcent[i] = self.DPCENT[i]
                self.dpaxis[i] = self.DPAXIS[i]
                self.dplaw[i] = self.DPLAW[i]
                self.dpzone[i] = self.DPZONE[i][2:]
                if(self.dpflag[i] <=4):
                    self.dpflag[i] = self.dpflag[i] + 4
        else:
            self.dp_com.setCurrentIndex(0)

        if (str(self.LDSIMTYPE) != a):#非定常计算类型
            self.ld_comsimtype.setCurrentIndex(int(self.LDSIMTYPE))
        else:
            self.ld_comsimtype.setCurrentIndex(0)

        if (str(self.TLTYPE) != a):#湍流模型
            if(int(self.TLTYPE) == 0):
                pass
            elif(int(self.TLTYPE) == 1 or int(self.TLTYPE) == 2):
                self.ld_comtltype.setCurrentIndex(int(self.TLTYPE)-1)
        else:
            self.ld_comtltype.setCurrentIndex(0)
        if(self.LDTYPE != a):
            if(int(self.LDTYPE) ==0 or int(self.LDTYPE) ==1):#流动类型
                self.ld_comldtype.setCurrentIndex(int(self.LDTYPE))
            elif(int(self.LDTYPE) ==3):
                self.ld_comldtype.setCurrentIndex(2)
        else:
            self.ld_comldtype.setCurrentIndex(0)

        if (str(self.XUSUAN) != a):#是否续算
            self.ld_comxusuan.setCurrentIndex(int(self.XUSUAN))
        else:

            self.ld_comxusuan.setCurrentIndex(0)

        if (str(self.LLMA) != a):#来流马赫数
            self.ll_textma.setText(self.LLMA)
        else:

            self.ll_textma.clear()

        if (str(self.LLYJ) != a):#来流迎角
            self.ll_textyingjiao.setText(self.LLYJ)
        else:

            self.ll_textyingjiao.clear()

        if (str(self.LLLNS) != a):#来流雷诺数
            self.ll_textleinuo.setText(self.LLLNS)
        else:
            self.ll_textleinuo.clear()

        if (str(self.LLCKCD) != a):#雷诺数参考长度
            self.ll_textleinuocd.setText(self.LLCKCD)
        else:
            self.ll_textleinuocd.clear()

        if (str(self.QDCD) != a):#气动力矩长度
            self.qd_textchangdu.setText(self.QDCD)
        else:
            self.qd_textchangdu.clear()

        if (str(self.QDMJ) != a):#气动面积
            self.qd_textmianji.setText(self.QDMJ)
        else:
            self.qd_textmianji.clear()

        if (str(self.QDZX) != a):#气动中心坐标
            self.qd_textzhongxin.setText(self.QDZX)
        else:
            self.qd_textzhongxin.clear()

        if (str(self.QJTJ) != a):#时间推进方式
            self.qj_comtuijin.setCurrentIndex(int(self.QJTJ))
        else:
            self.qj_comtuijin.setCurrentIndex(0)

        if (str(self.QJDL) != a):#对流通量
            self.qj_comduiliu.setCurrentIndex(int(self.QJDL))
        else:
            self.qj_comduiliu.setCurrentIndex(0)

        if (str(self.YXCANZHI) != a):#残值显示
            self.yx_textcancha.setText(self.YXCANZHI)
        else:
            self.yx_textcancha.clear()

        if (str(self.YXJIEGUO) != a):#结果保存步数
            self.yx_textjieguo.setText(self.YXJIEGUO)
        else:
            self.yx_textjieguo.clear()

        if (str(self.YXXUSUAN) != a):#续算保存步数
            self.yx_xusuan.setText(self.YXXUSUAN)
        else:
            self.yx_xusuan.clear()

        if(self.ld_comsimtype.currentIndex()==0):#求解器设置
            self.opendcwin()
            if (str(self.JSINNER) != a):
                self.dcwin.textinner.setText(self.JSINNER)
            else:
                self.dcwin.textinner.clear()
            if (str(self.JSCANZHI) != a):
                self.dcwin.textcancha.setText(self.JSCANZHI)
            else:
                self.dcwin.textcancha.clear()
        elif(self.ld_comsimtype.currentIndex()==1):
            self.opendcwin()
            if (str(self.JSOUT) != a and str(self.JSNT) != a):
                #zqnum = float(self.JSOUT)/float(self.JSNT)
                self.dcwin.textnt.setText(str(self.JSNT))
                self.dcwin.texttime.setText(str(float(self.DELT)*float(self.JSNT)))
            else:
                self.dcwin.textnt.clear()
                self.dcwin.texttime.clear()
            if (str(self.JSINNER) != a):
                self.dcwin.textinner.setText(self.JSINNER)
            else:
                self.dcwin.textinner.clear()

            if (str(self.JSCANZHI) != a):
                self.dcwin.textcancha.setText(self.JSCANZHI)
            else:
                self.dcwin.textcancha.clear()

            if (str(self.JSOUT) != a):
                self.dcwin.textout.setText(self.JSOUT)
            else:
                self.dcwin.textout.clear()
            if (str(self.JSINONE) != a):
                self.dcwin.textinone.setText(self.JSINONE)
            else:
                self.dcwin.textinone.clear()

        if (str(self.QJCFL) != a):#CFL数
            self.qj_textcfl.setText(self.QJCFL)
        else:
            self.qj_textcfl.clear()

        if (str(self.QJCFL3) != a):#CFL调节参数
            self.qj_textcfl3.setText(self.QJCFL3)
        else:
            self.qj_textcfl3.clear()
        (QtWidgets.QMessageBox.information(self, '信息提示对话框',
                                            '数据读取完成',
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No))

    def hyfill(self):
        if (self.hy_comnum.currentIndex() >= 1):
            self.hy_lcom1.setCurrentIndex(int(self.leftlist[0])-1)
            self.hy_rcom1.setCurrentIndex(int(self.rightlist[0])-1)
            self.hy_ltext1.setText(str(self.leftinlist[0]))
            self.hy_rtext1.setText(str(self.rightinlist[0]))
        if (self.hy_comnum.currentIndex() >= 2):
            self.hy_lcom2.setCurrentIndex(int(self.leftlist[1])-1)
            self.hy_rcom2.setCurrentIndex(int(self.rightlist[1])-1)
            self.hy_ltext2.setText(str(self.leftinlist[1]))
            self.hy_rtext2.setText(str(self.rightinlist[1]))
        if (self.hy_comnum.currentIndex() >= 3):
            self.hy_lcom3.setCurrentIndex(int(self.leftlist[2])-1)
            self.hy_rcom3.setCurrentIndex(int(self.rightlist[2])-1)
            self.hy_ltext3.setText(str(self.leftinlist[2]))
            self.hy_rtext3.setText(str(self.rightinlist[2]))
        if (self.hy_comnum.currentIndex() >=4):
            self.hy_lcom4.setCurrentIndex(int(self.leftlist[3])-1)
            self.hy_rcom4.setCurrentIndex(int(self.rightlist[3])-1)
            self.hy_ltext4.setText(str(self.leftinlist[3]))
            self.hy_rtext4.setText(str(self.rightinlist[3]))
        if (self.hy_comnum.currentIndex() == 5):
            self.hy_lcom5.setCurrentIndex(int(self.leftlist[4])-1)
            self.hy_rcom5.setCurrentIndex(int(self.rightlist[4])-1)
            self.hy_ltext5.setText(str(self.leftinlist[4]))
            self.hy_rtext5.setText(str(self.rightinlist[4]))


    def hysplit(self,hy):
        s = hy.split(':')
        s = s[0].split('(')
        left = s[0]
        s = s[1].split(')')
        leftin = s[0]
        s = hy.split(':')
        s = s[1].split('(')
        right = s[0]
        s = s[1].split(')')
        rightin = s[0]
        return left, leftin,right,rightin

    #保存配置文件
    def savecfg(self):
        if(self.caselocation == '' or self.caselocation == 'C:'):
            (QtWidgets.QMessageBox.information(self, '信息提示对话框',
                                               '请先选择网格文件',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No))
            return 0
        else:
            filename = self.caselocation + '\\parms.cfg2'
            try:
                with open(filename, 'w') as file:

                    file.write('#MCFV 2\n')
                    file.write('#PCFV 1\n\n')

                    if(self.wg_qunum.text().split()[0].isdigit()):#检测网格文件输入
                        file.write('#NMSH  ' + str(self.wg_qunum.text().split()[0]) + '\n')
                    else:
                        self.sendmessege(self.label_3.text())
                        return 0

                    file.write('#MTYP  ')#网格类型
                    for i in range(int(self.wg_qunum.text().split()[0])-1):
                        file.write('1 ')
                    file.write('1\n')

                    if(len(self.wg_bianjienum.text().split()) == int(self.wg_qunum.text().split()[0])):#边界数
                        file.write(self.strfrom(self.label_5,self.wg_bianjienum,'#NMRK  '))
                    else:
                        self.sendmessege(self.label_5.text())
                        return 0

                    if (len(self.wg_qunum_2.text().split()) == int(self.wg_qunum.text().split()[0])):#分区数
                        file.write(self.strfrom(self.label_7, self.wg_qunum_2, '#NPRT  '))
                    else:
                        self.sendmessege(self.label_7.text())
                        return 0

                    if(self.fy_comtype.currentIndex() == 0):#坐标系偏移量
                        if(self.strfrom(self.label_wgpy,self.wg_painyi,'#TRNS  ') !=0):
                            file.write(self.strfrom(self.label_wgpy,self.wg_painyi,'#TRNS  '))
                        else:
                            return 0
                    else:
                        pass

                    file.write('\n')

                    if(self.gz_radwhole.isChecked()):#编写滚转运动
                        file.write('#NCSY  1\n')
                    elif(self.gz_radpart.isChecked()):
                        file.write('#NCSY  2\n')

                    if(self.dp_com.currentIndex()==0):#编写舵偏运动
                        pass
                    else:
                        file.write('#NROT  ' + str(self.dp_com.currentIndex()) + '\n')

                    if(self.gz_radwhole.isChecked()):#编写CSCY
                        if(self.checkonenum(self.gz_law,self.gz_zhuansu)):
                            file.write('#CSYS #ROTX(1 ')
                            file.write(self.gz_law.text().strip() + ')')
                            if(self.fy_comtype.currentIndex() == 1):
                                file.write(' #ZONE(')
                                file.write(self.wg_qunum.text().strip() + ' ')
                                for i in range(int(self.wg_qunum.text().strip())-1):
                                    file.write(str(1+i) + ' ')
                                file.write(self.wg_qunum.text().strip() + ')\n')
                            elif(self.fy_comtype.currentIndex() == 0):
                                file.write(' #ROT')
                                if(self.fy_comaxis.currentIndex() == 0):
                                    file.write('Y(')
                                elif(self.fy_comaxis.currentIndex() == 1):
                                    file.write('Z(')
                                file.write('2 ')
                                if(self.checkonenum(self.fy_textbalance,self.fy_balance)):
                                    file.write(self.fy_textbalance.text().strip())
                                file.write(' ')
                                if(self.checkonenum(self.fy_textzhenfu, self.fy_zhenfu)):
                                    file.write(self.fy_textzhenfu.text().strip())
                                file.write(' ')
                                if (self.checkonenum(self.fy_textplv, self.fy_plv)):
                                    file.write(self.fy_textplv.text().strip())
                                file.write(' ')
                                if (self.checkonenum(self.fy_textxiangwei, self.fy_xiangwei)):
                                    file.write(self.fy_textxiangwei.text().strip())
                                    file.write(')')
                                file.write(' #ZONE(')
                                file.write(self.wg_qunum.text().strip() + ' ')
                                for i in range(int(self.wg_qunum.text().strip()) - 1):
                                    file.write(str(1 + i) + ' ')
                                file.write(self.wg_qunum.text().strip() + ')\n')
                        else:
                            self.sendmessege(self.gz_zhuansu.text())
                    elif(self.gz_radpart.isChecked()):
                        if (self.checkonenum(self.gz_law, self.gz_zhuansu)):
                            file.write('#CSYS #ROTX(1 ')
                            file.write(self.gz_law.text().strip() + ')')
                            if (self.fy_comtype.currentIndex() == 1):
                                file.write(' #ZONE(')
                                if(self.gz_zone.text().strip() == ''):
                                    self.sendmessege(self.label_gzzone.text())
                                    return 0
                                else:
                                    file.write(str(len(self.gz_zone.text().split())) + ' ')
                                    file.write(self.matchtest(self.gz_zone.text()))
                                    file.write(')\n')
                            elif (self.fy_comtype.currentIndex() == 0):
                                file.write(' #ROT')
                                if (self.fy_comaxis.currentIndex() == 0):
                                    file.write('Y(')
                                elif (self.fy_comaxis.currentIndex() == 1):
                                    file.write('Z(')
                                file.write('2 ')
                                if (self.checkonenum(self.fy_textbalance, self.fy_balance)):
                                    file.write(self.fy_textbalance.text().strip())
                                file.write(' ')
                                if (self.checkonenum(self.fy_textzhenfu, self.fy_zhenfu)):
                                    file.write(self.fy_textzhenfu.text().strip())
                                file.write(' ')
                                if (self.checkonenum(self.fy_textplv, self.fy_plv)):
                                    file.write(self.fy_textplv.text().strip())
                                file.write(' ')
                                if (self.checkonenum(self.fy_textxiangwei, self.fy_xiangwei)):
                                    file.write(self.fy_textxiangwei.text().strip())
                                    file.write(')')
                                file.write(' #ZONE(')
                                if (self.gz_zone.text().strip() == ''):
                                    self.sendmessege(self.label_gzzone.text())
                                    return 0
                                else:
                                    file.write(str(len(self.gz_zone.text().split())) + ' ')
                                    file.write(self.matchtest(self.gz_zone.text()))
                                    file.write(')\n')
                            file.write('#CSYS #ROTX(1 0)')
                            if (self.fy_comtype.currentIndex() == 1):
                                file.write(' #ZONE(')
                                if(self.gz_zone.text().strip() == ''):
                                    self.sendmessege(self.label_gzzone.text())
                                    return 0
                                else:
                                    zonlist = []
                                    for i in  range(int(self.wg_qunum.text())):
                                        checkreuslt = str(i) in self.matchtest(self.gz_zone.text())
                                        if(i != 0 and checkreuslt==False):
                                            zonlist.append(str(i))
                                    file.write(str(len(zonlist)) + ' ')
                                    for i in range(len(zonlist)-1):
                                        file.write(zonlist[i]+' ')
                                    file.write(zonlist[-1])
                                    file.write(')\n')
                            elif (self.fy_comtype.currentIndex() == 0):
                                file.write(' #ROT')
                                if (self.fy_comaxis.currentIndex() == 0):
                                    file.write('Y(')
                                elif (self.fy_comaxis.currentIndex() == 1):
                                    file.write('Z(')
                                file.write('2 ')
                                if (self.checkonenum(self.fy_textbalance, self.fy_balance)):
                                    file.write(self.fy_textbalance.text().strip())
                                file.write(' ')
                                if (self.checkonenum(self.fy_textzhenfu, self.fy_zhenfu)):
                                    file.write(self.fy_textzhenfu.text().strip())
                                file.write(' ')
                                if (self.checkonenum(self.fy_textplv, self.fy_plv)):
                                    file.write(self.fy_textplv.text().strip())
                                file.write(' ')
                                if (self.checkonenum(self.fy_textxiangwei, self.fy_xiangwei)):
                                    file.write(self.fy_textxiangwei.text().strip())
                                    file.write(')')
                                file.write(' #ZONE(')
                                if (self.gz_zone.text().strip() == ''):
                                    self.sendmessege(self.label_gzzone.text())
                                    return 0
                                else:
                                    zonlist = []
                                    for i in range(int(self.wg_qunum.text())):
                                        checkreuslt = str(i) in self.matchtest(self.gz_zone.text())
                                        if (i != 0 and checkreuslt == False):
                                            zonlist.append(str(i))
                                    file.write(str(len(zonlist)) + ' ')
                                    for i in range(len(zonlist) - 1):
                                        file.write(zonlist[i] + ' ')
                                    file.write(zonlist[-1])
                                    file.write(')\n')
                        else:
                            self.sendmessege(self.gz_zhuansu.text())

                    if(self.dp_com.currentIndex()>0):#舵偏运动数据填写

                        for i in range(self.dp_com.currentIndex()):
                            if(self.dpaxis[i] == 0):
                                self.sendmessege('舵偏运动')
                                return 0
                        for i in range(self.dp_com.currentIndex()):
                            file.write('#ROTA #CENT(')
                            file.write(str(self.dpcent[i]))
                            file.write(') #AXIS(')
                            file.write(self.dpaxis[i])
                            file.write(') #RPOP(')
                            file.write(self.dplaw[i])
                            file.write(') #ZONE(')
                            file.write(str(len(str(self.dpzone[i]).split())) + ' ')
                            file.write(self.dpzone[i])
                            file.write(')\n')
                    if(self.hy_comnum.currentIndex()==0):
                        pass
                    else:
                        self.readhy()
                        file.write('\n\n')
                        file.write('#NSLD  ' + str(self.hy_comnum.currentIndex()) + '\n')
                        for i in range(self.hy_comnum.currentIndex()):
                            file.write('#SLID  ')

                            file.write(str(self.hyleftlist[i]+1) + '(' + str(self.hylefttext[i])+ ')')

                            file.write(':' + str(self.hyrightlist[i]+1) + '(' + str(self.hyrighttext[i])+ ')\n')


                    if(self.ld_comsimtype.currentIndex() == 1):#非定常计算
                        if(self.dcwin.textout.text() == ''):
                            self.sendmessege(self.dcwin.labelouter.text())
                            return 0
                        else:
                            file.write('#UNST #NSTP(')
                            file.write(self.dcwin.textout.text())
                            file.write(') #DELT(')
                        if(self.dcwin.texttime.text() == ''):
                            self.sendmessege(self.dcwin.labeltime.text())
                            return 0
                        else:
                            if(self.dcwin.textnt.text() == ''):
                                self.sendmessege(self.dcwin.labelnt.text())
                                return 0
                            else:
                                s = float(self.dcwin.textout.text())/float(self.dcwin.textnt.text())
                                file.write(str(float(self.dcwin.texttime.text())/s))
                                file.write(')\n')

                    file.write('\n&FLOW_ALL\n')

                    if(self.ld_comldtype.currentIndex() <=1):#流动类型
                        file.write('PHYSICAL_PROBLEM             =           ' + str(self.ld_comldtype.currentIndex()) + '\n')
                    elif(self.ld_comldtype.currentIndex() == 2):
                        file.write('PHYSICAL_PROBLEM             =           3\n')

                    if(self.ld_comldtype.currentIndex() == 2):#湍流类型
                        file.write('TURB_MODEL                   =           ' + str(self.ld_comtltype.currentIndex()+1) + '\n')
                    elif(self.ld_comldtype.currentIndex() <=1):
                        file.write('TURB_MODEL                   =           0\n')

                    file.write('IS_RESTART_SOL               =           ' + str(self.ld_comxusuan.currentIndex()) + '\n')#是否续算
                    file.write('\n')

                    if(self.ll_textma.text() == ''):#来流马赫数
                        self.sendmessege(self.label_llma.text())
                        return 0
                    else:
                        file.write('FLOW_MACH                    =    ' + str(self.ll_textma.text()) + '\n')

                    if (self.ll_textyingjiao.text() == ''):#来流迎角
                        self.sendmessege(self.label_llyingjaio.text())
                        return 0
                    else:
                        file.write('FLOW_AOA                     =    ' + str(self.ll_textyingjiao.text()) + '\n')

                    if (self.ll_textleinuo.text() == ''):#来流雷诺数
                        self.sendmessege(self.label_llleinuo.text())
                        return 0
                    else:
                        file.write('REYNOLDS_NUMBER              =    ' + str(self.ll_textleinuo.text()) + '\n')

                    if (self.ll_textleinuocd.text() == ''):#雷诺数参考长度
                        self.sendmessege(self.label_llleinuochangdu.text())
                        return 0
                    else:
                        file.write('REYNOLDS_LENGTH              =    ' + str(self.ll_textleinuocd.text()) + '\n')

                    file.write('\n')

                    if (self.qd_textchangdu.text() == ''):#气动力矩长度
                        self.sendmessege(self.label_qdcd.text())
                        return 0
                    else:
                        file.write('AERO_REFLEN                  =    ' + str(self.qd_textchangdu.text()) + '\n')

                    if (self.qd_textmianji.text() == ''):#气动面积
                        self.sendmessege(self.label_qdmj.text())
                        return 0
                    else:
                        file.write('AERO_REFAREA                 =    ' + str(self.qd_textmianji.text()) + '\n')

                    if (self.qd_textzhongxin.text() == ''):#气动中心
                        self.sendmessege(self.label_qdzx.text())
                        return 0
                    else:
                        file.write('AERO_REFCENT                 =    ' + str(self.qd_textzhongxin.text()) + '\n')

                    file.write('AERO_REFCSID                 =           1' +'\n')#气动坐标系
                    file.write('\n')

                    file.write('CONV_NUM_METHOD_FLOW         =           ' + str(self.qj_comduiliu.currentIndex()) + '\n')#对流通量
                    file.write('TEMPORAL_SCHEME              =           ' + str(self.qj_comtuijin.currentIndex()) + '\n')#时间推进格式

                    if(self.qj_textcfl.text() == ''):#CFL数
                        self.sendmessege(self.label_qjcfl.text())
                        return 0
                    else:
                        file.write('CFL_NUMBER                   =    ')
                        file.write(str(self.qj_textcfl.text()) + '\n')

                    file.write('CFL_RAMP                     =    ')#默认输出cflramp
                    file.write('1.0 100.0 1.0\n')
                    file.write('\n')

                    file.write('UNSTEADY_SIMULATION          =           ' + str(self.ld_comsimtype.currentIndex()) + '\n')#计算类型

                    if(self.ld_comsimtype.currentIndex() == 1):#求解器设置
                        if(self.dcwin.textout.text() == ''):
                            self.sendmessege(self.dcwin.labelouter.text())
                            return 0
                        else:
                            file.write('NITER_OUTER                  =         ' + str(self.dcwin.textout.text()) + '\n')
                        if(self.dcwin.textinner.text()  == ''):
                            self.sendmessege(self.dcwin.labelinner.text())
                        else:
                            file.write('NITER_INNER                  =         ' + str(self.dcwin.textinner.text()) + '\n')
                        if (self.dcwin.textinone.text() == ''):
                            self.sendmessege(self.dcwin.labelinone.text())
                        else:
                            file.write('NITER_INONE                  =        ' + str(self.dcwin.textinone.text()) + '\n')
                    elif(self.ld_comsimtype.currentIndex() == 0):
                        file.write('NITER_OUTER                  =         1\n')
                        file.write('NITER_INNER                  =         ' + str(self.dcwin.textinner.text()) + '\n')
                        file.write('NITER_INONE                  =        1\n')

                    if(self.dcwin.textcancha.text() == ''):#残差收敛量级
                        self.sendmessege(self.dcwin.labelcancha.text())
                        return 0
                    else:
                        file.write('RES_CONV_ORDER               =        ' + str(self.dcwin.textcancha.text()) + '\n')

                    file.write('\n')

                    if (self.yx_textcancha.text() == ''):#残差保存间隔
                        self.sendmessege(self.label_yxcc.text())
                        return 0
                    else:
                        file.write('NITER_RESHOW                 =           ' + str(self.yx_textcancha.text()) + '\n')

                    if(self.ld_comsimtype.currentIndex() == 0):#求解器设置
                        file.write('NITER_PRLOOP                 =         100000\n')
                    elif(self.ld_comsimtype.currentIndex() == 1):
                        if(self.dcwin.textnt.text() == ''):
                            self.sendmessege(self.dcwin.labelnt.text())
                            return 0
                        else:
                            file.write('NITER_PRLOOP                 =         ' + str(self.dcwin.textnt.text()) + '\n')

                    if (self.yx_textjieguo.text() == ''):#结果保存间隔
                        self.sendmessege(self.label_yxjieguo.text())
                        return 0
                    else:
                        file.write('NITER_RUSAVE                 =          ' + str(self.yx_textjieguo.text()) + '\n')

                    if (self.yx_xusuan.text() == ''):#续算保存间隔
                        self.sendmessege(self.label_yxxusuan.text())
                        return 0
                    else:
                        file.write('NITER_RESOLU                 =          ' + str(self.yx_xusuan.text()) + '\n')

                    file.write('/\n')
            except:
                self.sendmessege('参数设置')
            #file.close()
    def strfrom(self,label,text,index):
        if (text.text().strip() == ''):
            self.sendmessege(label.text())
            return 0
        else:

            if (self.matchtest(text.text()) == 'wrong'):
                self.sendmessege(self.label.text())
                return 0
            else:

                return index+self.matchtest(text.text())+'\n'
        pass

    def sendmessege(self,labelname):
        (QtWidgets.QMessageBox.information(self, '信息提示对话框',
                                           labelname + '设置存在错误',
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No))
    def matchtest(self,text):
        s = text.split()
        result = ''
        for i in range(len(s)-1):
                result = result +s[i] + ' '
        result = result + s[-1]
        return result
    def checkonenum(self,text,label):
        if(len(text.text().strip().split()) == 1):
            return True
        else:
            self.sendmessege(label.text())
            return False

    def setrange(self):
        self.wg_qunum.setFocusPolicy(QtCore.Qt.NoFocus)
        self.wg_bianjienum.setFocusPolicy(QtCore.Qt.NoFocus)
        regx = QRegExp("[-+]?\d{,3}[.]?\d{,3}[ ][-+]?\d{,3}[.]?\d{,3}[ ][-+]?\d{,3}[.]?\d{,3}")
        validator = QtGui.QRegExpValidator(regx, self.wg_painyi)
        self.wg_painyi.setValidator(validator)
        regx = QRegExp("[-+]?\d{,3}[.]?\d{,3}[ ][-+]?\d{,3}[.]?\d{,3}[ ][-+]?\d{,3}[.]?\d{,3}")
        validator = QtGui.QRegExpValidator(regx, self.qd_textzhongxin)
        self.qd_textzhongxin.setValidator(validator)
        regx = QRegExp("(\d{,3}\d{,3}[ ]\d{,3}\d{,3}[ ]\d{,3}\d{,3})+")
        validator = QtGui.QRegExpValidator(regx, self.wg_qunum_2)
        self.wg_qunum_2.setValidator(validator)
        validator = QtGui.QRegExpValidator(regx, self.gz_zone)
        self.gz_zone.setValidator(validator)





        self.hy_ltext1.setValidator(QtGui.QIntValidator(0, 65535))
        self.hy_ltext2.setValidator(QtGui.QIntValidator(0, 65535))
        self.hy_ltext3.setValidator(QtGui.QIntValidator(0, 65535))
        self.hy_ltext4.setValidator(QtGui.QIntValidator(0, 65535))
        self.hy_ltext5.setValidator(QtGui.QIntValidator(0, 65535))
        self.hy_rtext1.setValidator(QtGui.QIntValidator(0, 65535))
        self.hy_rtext2.setValidator(QtGui.QIntValidator(0, 65535))
        self.hy_rtext3.setValidator(QtGui.QIntValidator(0, 65535))
        self.hy_rtext4.setValidator(QtGui.QIntValidator(0, 65535))
        self.hy_rtext5.setValidator(QtGui.QIntValidator(0, 65535))

        self.gz_law.setValidator(QtGui.QDoubleValidator(-65535, 65535, 10))

        self.fy_textplv.setValidator(QtGui.QDoubleValidator(-65535, 65535, 10))
        self.fy_textxiangwei.setValidator(QtGui.QDoubleValidator(-65535, 65535, 10))
        self.fy_textzhenfu.setValidator(QtGui.QDoubleValidator(-65535, 65535, 10))
        self.fy_textbalance.setValidator(QtGui.QDoubleValidator(-65535, 65535, 10))

        self.ll_textleinuocd.setValidator(QtGui.QDoubleValidator(0, 65535, 10))
        self.ll_textleinuo.setValidator(QtGui.QDoubleValidator(0, 65535, 10))
        self.ll_textyingjiao.setValidator(QtGui.QDoubleValidator(-90, 90, 10))
        self.ll_textma.setValidator(QtGui.QDoubleValidator(0, 65535, 10))

        self.qd_textmianji.setValidator(QtGui.QDoubleValidator(0, 65535, 10))
        self.qd_textchangdu.setValidator(QtGui.QDoubleValidator(0, 65535, 10))

        self.qj_textcfl.setValidator(QtGui.QDoubleValidator(-65535, 65535, 10))

        self.yx_textjieguo.setValidator(QtGui.QIntValidator(1, 65535))
        self.yx_textcancha.setValidator(QtGui.QIntValidator(1, 65535))
        self.yx_xusuan.setValidator(QtGui.QIntValidator(1, 65535))

    def readhy(self):

        self.hyleftlist = []
        self.hyleftlist.append(self.hy_lcom1.currentIndex())
        self.hyleftlist.append(self.hy_lcom2.currentIndex())
        self.hyleftlist.append(self.hy_lcom3.currentIndex())
        self.hyleftlist.append(self.hy_lcom4.currentIndex())
        self.hyleftlist.append(self.hy_lcom5.currentIndex())
        self.hyrightlist = []
        self.hyrightlist.append(self.hy_rcom1.currentIndex())
        self.hyrightlist.append(self.hy_rcom2.currentIndex())
        self.hyrightlist.append(self.hy_rcom3.currentIndex())
        self.hyrightlist.append(self.hy_rcom4.currentIndex())
        self.hyrightlist.append(self.hy_rcom5.currentIndex())

        self.hylefttext = []
        self.hylefttext.append(self.hy_ltext1.text())
        self.hylefttext.append(self.hy_ltext2.text())
        self.hylefttext.append(self.hy_ltext3.text())
        self.hylefttext.append(self.hy_ltext4.text())
        self.hylefttext.append(self.hy_ltext5.text())
        self.hyrighttext = []
        self.hyrighttext.append(self.hy_rtext1.text())
        self.hyrighttext.append(self.hy_rtext2.text())
        self.hyrighttext.append(self.hy_rtext3.text())
        self.hyrighttext.append(self.hy_rtext4.text())
        self.hyrighttext.append(self.hy_rtext5.text())


    def readbainjiefile(self):

        if (self.locationcheck()):
            filepath = self.caselocation + '/RESULT'
            filename, type = QtGui.QFileDialog.getOpenFileNames(None, "请选择文件", filepath,
                                                                "Plt Files (*.plt);;All Files (*)")
            if (filename != []):
                self.sliceflag = False
                self.meshlist = []
                self.zhenntimeshlist = []
                self.bianjiename = []
                self.meshcomfill('RBC')
                for i in range(len(filename)):
                    if ('RBC' in filename[i]):
                        offset, cells, celltype, points, self.bianjiename, property, data = self.mb.meshplot(filename[i])
                        self.grid = pv.UnstructuredGrid(offset, cells, celltype, points)
                        for i in range(len(data) - 3):
                            self.grid.point_arrays[self.bianjiename[i + 3]] = property[i]
                        self.meshlist.append(self.grid)

        pass
    def plotmesh(self):#网格文件绘图
        try:
            self.readbainjiefile()
            self.bianjieplotter()
            self.plotter.reset_camera()
        except:
            self.sendmessege('结果文件')


    def bianjieplotter(self):
        self.plotter.clear()
        cpos = self.plotter.camera_position
        for index in self.meshlist:
            if (self.checkmesh.isChecked()):
                self.plotter.add_mesh(index, show_edges=True,
                                      scalars=self.bianjiename[self.combar.currentIndex() + 3])
            else:
                self.plotter.add_mesh(index, show_edges=False,
                                      scalars=self.bianjiename[self.combar.currentIndex() + 3])
            if (self.checkoutline.isChecked()):
                self.plotter.add_mesh(index.outline())
        self.plotter.camera_position = cpos
        self.plotter.show_axes()



    def sendemit(self):
        if(self.locationcheck()):
            if(os.path.exists(self.yx_exepath.text())):
                s = self.wg_qunum_2.text().split()
                qunumber = 0
                for i in s:
                    qunumber = int(i)+qunumber
                s = self.caselocation.split('/')
                s = self.caselocation.split('/'+s[-1])
                self.clickSignal.emit(s[0],int(qunumber),self.yx_exepath.text(),self.caselocation,0)
            else:
                self.sendmessege('求解器')
        else:
            pass
    def fillplotter(self,offset, cells, celltype, points, name, property, data):
        self.grid = pv.UnstructuredGrid(offset, cells, celltype, points)
        for i in range(len(data) - 3):
            self.grid.point_arrays[name[i + 3]] = property[i]
        self.gridlist.append(self.grid)
        self.sbsignal.emit()
    def czbianjie(self):
        self.czwin.close()
        self.plotmesh()
    def czinner(self):
        self.czwin.close()
        self.plottt()

    def meshcomfill(self,type):
        if(self.plottype == 0):
            if(self.combar.count() ==0):
                self.combar.clear()
                resultpath = self.caselocation + r'\RESULT'
                filename1 = glob.glob(resultpath + '\\*.plt')
                for i in range(len(filename1)):
                    if (type in filename1[i]):
                        offset, cells, celltype, points, name, property, data = self.mb.meshplot(filename1[i])
                        for i in range(3,len(name)):
                            self.combar.addItem(name[i])
                        self.combar.setCurrentIndex(0)
                        return 0
            elif(self.combar.count() !=0):
                return 0
        elif(self.plottype == 1):
            self.combar.clear()
            resultpath = self.caselocation + r'\RESULT'
            filename1 = glob.glob(resultpath + '\\*.plt')
            for i in range(len(filename1)):
                if (type in filename1[i]):
                    offset, cells, celltype, points, name, property, data = self.mb.meshplot(filename1[i])
                    for i in range(3, len(name)):
                        self.combar.addItem(name[i])
                    self.combar.setCurrentIndex(0)
                    break
        self.plottype = 0
    def meshinnercomfill(self,type):
        if (self.plottype == 1):

            if (self.combar.count() == 0):
                self.combar.clear()
                resultpath = self.caselocation + r'\RESULT'
                filename1 = glob.glob(resultpath + '\\*.plt')
                for i in range(len(filename1)):
                    if (type in filename1[i]):
                        grid, name1, type1 = self.ib.meshplot(filename1[i])
                        if (name1 != 0):
                            for i in range(0, len(name1)):
                                self.combar.addItem(name1[i])
                            self.combar.setCurrentIndex(0)
                            break
                        else:
                            pass

            elif (self.combar.count() != 0):

                return 0
        elif (self.plottype == 0):

            self.combar.clear()
            resultpath = self.caselocation + r'\RESULT'
            filename1 = glob.glob(resultpath + '\\*.plt')
            for i in range(len(filename1)):
                if (type in filename1[i]):
                    grid,name1,type1 = self.ib.meshplot(filename1[i])
                    if(name1 !=0):
                        for i in range(0, len(name1)):
                            self.combar.addItem(name1[i])
                        self.combar.setCurrentIndex(0)
                        break
                    else:
                        pass
        self.plottype = 1
    def closeEvent(self, event):
        if(self.dcwin.isVisible()):
            self.dcwin.close()
        if (self.czwin.isVisible()):
            self.czwin.close()
        if (self.slicewin.isVisible()):
            self.slicewin.close()
        if (self.dpwin.isVisible()):
            self.dpwin.close()





class readdata(QThread):
    datasignal= QtCore.pyqtSignal()
    def __int__(self):
        super(readdata, self).__init__()
        self.filename = []

    def run(self):
       self.mb1 = mb.buildmesh()
       for i in range(len(self.filename)):
           self.offset, self.cells, self.celltype, self.points, self.name, self.property, self.data = self.mb1.meshplot(self.filename[i])
       self.datasignal.emit()
    def getpath(self,path,num):
        self.filename = []
        if(num == 'bianjie'):

            for i in range(len(path)):
                if ('RBC' in path[i]):
                    self.filename.append(path[i])
        elif(num == 'inner'):
            for i in range(len(path)):
                if ('Rsu' in path[i]):
                    self.filename.append(path[i])






















