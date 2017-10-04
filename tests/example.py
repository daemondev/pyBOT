from PyQt5 import QtCore, QtGui, uic, QtWidgets
import sys
from FingerTabs import FingerTabWidget

app = QtWidgets.QApplication(sys.argv)
#tabs = QtWidgets.QTabWidget()
tabs = FingerTabWidget(width=100,height=25)
#tabs.setTabBar(FingerTabWidget(width=100,height=25))
digits = ['Thumb','Pointer','Rude','Ring','Pinky']
tabs.setStyleSheet("padding-bottom:0px; background-color:red;")

for i,d in enumerate(digits):
    widget =  QtWidgets.QLabel("Area #%s <br> %s Finger"% (i,d))
    tabs.addTab(widget, d)

tabs.setTabPosition(QtWidgets.QTabWidget.West)
tabs.show()
sys.exit(app.exec_())
