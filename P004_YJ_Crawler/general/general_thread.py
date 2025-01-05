# pack the func into thread
from threading import Thread
from PyQt5 import QtCore


class MyThread(QtCore.QThread):
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.daemon = True
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)


# func only contain the function name, no ()
# *args is the args where func requested
def thread_it(func, *args):
    # create thread
    t = Thread(target=func, args=args)
    # enable daemon !!!
    t.daemon = True
    # start the thread
    t.start()
    # block
    # t.join()
