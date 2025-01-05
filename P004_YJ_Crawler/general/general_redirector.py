import sys
from PyQt5 import QtWidgets, QtCore, QtGui  # pip install PyQt5
from general import general_thread
import time


# init param is the widget used as target output
class Redirector:
    def __init__(self, target):
        # save current output obj
        self.target = target
        self.stdoutbak = sys.stdout
        self.stderrbak = sys.stderr
        # redirect
        sys.stdout = self
        sys.stderr = self

    # Please notice that write/update method varies with different widget
    # should re-write according the widget
    # info is the output received by sys.stdout and sys.stderr
    # Should put the write into a single thread!!!!!!!!!!!!!!!
    def write(self, info):
        """
        # below comment part are implemented with tkinter ScrolledText
        # insert the info in last line
        self.target.insert('end', info)
        # show the new info
        self.target.update()
        # always locate at the last line
        self.target.see(tkinter.End)
        """
        # self.trigger.emit(info)
        general_thread.thread_it(self.myWrite, info)
        # self.myWrite(info)

    def update_text(self, message):
        self.target.insertPlainText(message)  # use insertPlainText to prevent the extra newline character

    def myWrite(self, info):
        # below comment part are implemented with PyQt textBrowser
        # insertPlainText only print plaintext
        self.target.insertPlainText(info)
        time.sleep(0.2)

        # update the screen
        QtWidgets.qApp.processEvents(
            QtCore.QEventLoop.ExcludeUserInputEvents)  # | QtCore.QEventLoop.ExcludeSocketNotifiers)
        # self.stdoutbak.write(info)

        # not recommended to use QtGui.QTextCursor in thread
        # cause modify UI in thread is not allowed?
        # will throw an warning while run in EXE mode
        self.target.moveCursor(QtGui.QTextCursor.End)

        # make sure the auto scroll effect
        self.target.ensureCursorVisible()

    def restoreStd(self):
        # recover source output
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak

    def flush(self):
        pass
