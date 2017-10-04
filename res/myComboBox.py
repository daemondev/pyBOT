class MyCombo(QComboBox):

    def __init__(self, parent=None):
        super(MyCombo, self).__init__(parent)
        self.setEditable(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            print "return pressed"
        else:
            QComboBox.keyPressEvent(self, event)

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            print "tab pressed"
            return False
        return QWidget.event(self, event)

class Form_1(QDialog):

    def __init__(self, parent=None):
        super(Form_1, self).__init__(parent)
        self.combo = MyCombo()
        self.line = QLineEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.combo)
        layout.addWidget(self.line)
        self.setLayout(layout)