from PyQt5 import QtCore, QtGui, uic, QtWidgets
from FingerTabs import FingerTabWidget
import sys
form, base = uic.loadUiType("form.ui")
#from form import Ui_MainWindow
#form = Ui_MainWindow()


class MyWidget (QtWidgets.QMainWindow):
    def __init__(self, mixin_arg, **kwds):
        super().__init__(**kwds)
        #self.setupUi(self)

    def alert(self):
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MyWidget(None)

    #tabs = QtWidgets.QTabWidget(form)
    tabs = FingerTabWidget(form,width=100,height=25)
    #tabs.setTabBar(form, FingerTabWidget(width=100,height=25))
    digits = ['Thumb','Pointer','Rude','Ring','Pinky']
    #tabs.setStyleSheet("padding-bottom:0px; background-color:red;")

    for i,d in enumerate(digits):
        widget =  QtWidgets.QLabel("Area #%s <br> %s Finger"% (i,d))
        tabs.addTab(widget, d)

    tabs.setTabPosition(QtWidgets.QTabWidget.West)
    form.show()
    app.exec_()
