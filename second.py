from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
from gtts import gTTS

class Second(QWidget):
    def __init__(self, storage):
        super().__init__()
        uic.loadUi('second.ui', self)

        ## Set up functionality
        self.storage = storage
        self.func = DictEditFunction(self.storage)
        # Check answer box is empty
        self.enter_btn.clicked.connect(lambda: self.handle_entry_enter(
            self.word_entry.text(), self.definition_entry.toPlainText()))
    
    def handle_entry_enter(self, word, meaning):
        if not self.func.check_data_enterd(word, meaning):
            self.func.append_dict_list(word)
            common = []
            if self.formal_chkbox.isChecked():
                common.append(1)
            else:
                common.append(0)
            if self.informal_chkbox.isChecked():
                common.append(1)
            else:
                common.append(0)
            if self.written_chkbox.isChecked():
                common.append(1)
            else:
                common.append(0)
            if self.spoken_chkbox.isChecked():
                common.append(1)
            else:
                common.append(0)
            self.func.add_new_word(self.word_entry.text(), self.definition_entry.toPlainText(), common,
                                   self.usage_entry.toPlainText(), self.example_entry.toPlainText(), self.chinese_entry.toPlainText(),
                                   [self.synonym_entry1.toPlainText(), self.synonym_entry2.toPlainText(), self.synonym_entry3.toPlainText()]
                                   )
            self.word_entry.clear()
            self.definition_entry.clear()
            self.formal_chkbox.setChecked(False)
            self.informal_chkbox.setChecked(False)
            self.written_chkbox.setChecked(False)
            self.spoken_chkbox.setChecked(False)
            self.usage_entry.clear()
            self.example_entry.clear()
            self.chinese_entry.clear()
            self.synonym_entry1.clear()
            self.synonym_entry2.clear()
            self.synonym_entry3.clear()

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
    
    def append_dict_list(self, word):
        self.storage.current_dict.append(word)

    def check_word_appear(self, word):
        word = word.title()
        if word in self.storage.dictionary:
            return True
        return

    def add_new_word(self, word, defin, common, usage, example, chinese, syn):
        path = self.text_to_speech(word)
        self.storage.play_sound(path)
        temp_dict = {
            "definition" : defin,
            "common" : common,
            "usage" : usage,
            "example" :  example,
            "chinese" : chinese,
            "synonyms" : syn,
            "state" : 1,
            "add time" : time.strftime("%Y-%m-%d", time.localtime(time.time())),
            "test time" : time.strftime("%Y-%m-%d", time.localtime(time.time())),
            "pronunciation" : path
        }
        self.storage.dictionary[word] = temp_dict

    def text_to_speech(self, word):
        speech = gTTS(text = word)
        path = f".//Sound Track//{word}.mp3"
        speech.save(path)
        return path
    