from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class Second(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('second.ui', self)



class DictEditFunction():
    def __init__(self) -> None:
        pass

    def check_data_enterd(self, word, mean):
        if word and mean:
            return True
        message = QMessageBox()
        message.setText("Please enter an answer!")
        message.exec_()
        return
    
