from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from constant import *

class Second(QWidget):
    def __init__(self, storage):
        super().__init__()
        uic.loadUi('second.ui', self)

        ## Set up functionality
        self.storage = storage
        self.func = DictEditFunction(self.storage)
        # Check answer box is empty
        self.enter_btn.clicked.connect(lambda: self.handle_entry_enter(self.word_entry.text(), self.meaning_entry.toPlainText()))
    
    def handle_entry_enter(self, word, meaning):
        if not self.func.check_data_enterd(word, meaning):
            self.func.append_dict_list(word, meaning)
            self.func.append_state_list(word)
            self.word_entry.clear()
            self.meaning_entry.clear()

class DictEditFunction():
    def __init__(self, storage):
        self.storage = storage

    def check_data_enterd(self, word, mean):
        if not word:
            message = QMessageBox()
            message.setText("Please type a word")
            message.exec_()
            return True
        elif not mean:
            message = QMessageBox()
            message.setText("Please enter the meaning of the word")
            message.exec_()
            return True
        if self.check_word_appear(word):
            message = QMessageBox()
            message.setText("This word already existed in the dictionary")
            message.exec_()
            return True
    
    def append_dict_list(self, word, meaning):
        self.storage.dict[word] = meaning
        self.storage.current_dict.append(word)

    def check_word_appear(self, word):
        if word in self.storage.dict:
            return True
        return

    def append_state_list(self, word):
        self.storage.state[word] = True