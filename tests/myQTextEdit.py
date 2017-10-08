class MyTextEdit(QTextEdit):
   def __init__(self, *args):
   QTextEdit.__init__(self, *args)

   keyPressedSignal = pyqtSignal(int, bool, bool)

   def keyPressEvent(self, event):
      shift = False
      ctrl = False
      if (event.modifiers() & Qt.ShiftModifier):
         shift = True
      if (event.modifiers() & Qt.ControlModifier):
         ctrl = True
      self.keyPressedSignal.emit(event.key(), shift, ctrl)
"""
modifiers = event.modifiers()
if (modifiers & Qt.ShiftModifier)
...
if (modifiers & Qt.ControlModifier)
...
"""

class MessageTextEdit(QTextEdit):
    def __init__(self,  parent):
        super(MessageTextEdit,  self).__init__(parent)

        self.parent = parent
        self.__sendMessageOnReturn = False

    def sendMessageOnreturn(self):
        return self.__sendMessageOnReturn

    def setSendMessageOnReturn(self,  state):
        self.__sendMessageOnReturn = state

    def keyPressEvent(self,  event):
        if self.__sendMessageOnReturn:
            if event.key() == Qt.Key_Return:
                if event.modifiers() == Qt.ControlModifier:
                    event = QKeyEvent(QEvent.KeyPress,  Qt.Key_Return, Qt.NoModifier)
                else:
                    self.emit(SIGNAL("sendMessage"))
                    return

    QTextEdit.keyPressEvent(self,  event)
