from PyQt5 import QtWidgets
from mainwindow import MainWindow
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
#self.plotter = pv.QtInteractor(self.frame)
       #self.horizontalLayout_2.addWidget(self.plotter.interactor)
    '''import pyvistaqt as pv
    self.plotter = pv.QtInteractor(self.frame)
    self.gridLayout_2.addWidget(self.plotter.interactor, 0, 1, 1, 1)
    import pyvistaqt as pv
        self.plotter = pv.QtInteractor(self.frame)
        self.horizontalLayout.addWidget(self.plotter.interactor)'''

