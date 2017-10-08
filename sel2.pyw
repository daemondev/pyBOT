from PyQt5 import QtCore, QtGui, uic, QtWidgets
import sys

source = ""
try:
    form, base = uic.loadUiType("form.ui")
    source = "ui"
except Exception as e:
    from form import Ui_MainWindow
    form = Ui_MainWindow
    source = "class"


class MyWidget (QtWidgets.QMainWindow, form):
    def __init__(self, mixin_arg, **kwds):
        super().__init__(**kwds)
        self.setupUi(self)
        self.__bind__()

    def __bind__(self):
        self.btnSend.clicked.connect(self.changeText)

    def changeText(self):
        global source
        self.lblDebug.setText(source + " - " + self.txtCommand.text())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MyWidget(None)
    form.show()
    app.exec_()
