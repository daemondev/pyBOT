from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class FingerTabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        self.tabSize = QtCore.QSize(kwargs.pop('width'), kwargs.pop('height'))
        super(FingerTabWidget, self).__init__(*args, **kwargs)
        #self.setStyleSheet(open("style.qss", "r").read())

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        #painter = QtGui.QPainter(self)
        #option = QtWidgets.QStyleOptionTab()
        option = QtWidgets.QStyleOptionTabWidgetFrame()
        #option = QtWidgets.QStyleOptionTabBarBase()


        #buttonReply = QMessageBox.question(self, 'PyQt5 message', str(self.count()) + " - " + "Do you like PyQt5?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #if buttonReply == QMessageBox.Yes:
            #print('Yes clicked.')
        #else:
            #print('No clicked.')


        painter.begin(self)
        for index in range(self.count()):
            self.initStyleOption(option)
            tabRect = self.tabRect(index)
            tabRect.moveLeft(10)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, option)
            painter.drawText(tabRect, QtCore.Qt.AlignVCenter | QtCore.Qt.TextDontClip, self.tabText(index));
        painter.end()
    def tabSizeHint(self,index):
        return self.tabSize
