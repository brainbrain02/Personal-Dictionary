from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from constant import *
import random

class First(QWidget):
    def __init__(self, storage):
        super().__init__()
        uic.loadUi('first.ui', self)

        ### Main function setup
        self.storage = storage
        self.func = FlashCardFunction(self.storage)
        # Open current dictionary
        current_word = self.func.choose_word(self.storage.current_dict)
        if current_word:
            self.update_word_information(current_word)
        else:
            message = QMessageBox()
            message.setText("Can not read the current dictionary!")
            message.exec_()

        # Check answer box is empty
        self.enter_btn.clicked.connect(
            lambda: self.handle_ans_enter(self.ans_entry.text())
            )

        # Install an event filter to capture key events
        self.ans_entry.installEventFilter(self)

    def update_word_information(self, list):
        self.mean_lab2.setText(list[0])
        self.common_lab2.setText(list[1])
        self.usage_lab2.setText(list[2])
        self.synonym_lab2.setText(list[3][0])
        self.synonym_lab3.setText(list[3][1])
        self.synonym_lab4.setText(list[3][2])

    def handle_ans_enter(self, ans):
        # Check answer entered
        if not self.func.check_answer_enterd(ans):
            # Check answer correctness
            word = self.func.check_ans_correct(ans)
            if word:
                self.func.show_message_box(
                    f"Wrong Answer!\nThe answer should be: {word}\n"
                    )
                # loop = QEventLoop()
                # QTimer.singleShot(2000, loop.quit)
                # loop.exec_()
            self.ans_entry.clear()
            self.storage.current_dict.remove(self.func.word)
            self.storage.handle_empty_dict(self.storage.dictionary)
            next_word = self.func.choose_word(self.storage.current_dict)
            if next_word:
                self.update_word_information(next_word)
            else:
                message = QMessageBox()
                message.setText("Can not read the next word!")
                message.exec_()

    def eventFilter(self, obj, event):
        if obj == self.ans_entry and event.type() == event.KeyPress \
            and event.key() == Qt.Key_Return:
            self.handle_ans_enter(self.ans_entry.text())
            return True
        return super().eventFilter(obj, event)

class FlashCardFunction():
    def __init__(self, storage):
        self.storage = storage

    def check_answer_enterd(self, ans):
        if not ans:
            message = QMessageBox()
            message.setText("Please enter an answer!")
            message.exec_()
            return True

    def choose_word(self, dict_list):
        self.word = random.choice(dict_list)
        self.meaning = self.storage.dictionary[self.word].get("definition")
        return [
            self.storage.dictionary[self.word].get("definition"),
            self.storage.dictionary[self.word].get("common"),
            self.storage.dictionary[self.word].get("usage"),
            self.storage.dictionary[self.word].get("synonyms")
        ]

    def check_ans_correct(self, answer):
        ans = answer.lower()
        if ans != self.word:
            self.storage.wrong_answer_list.append(self.word)
            return self.word
        else:
            self.storage.correct_answer_list.append(self.word)
            return
    
    def form_pair(self, list):
        pair = f"{list[0]}:{list[1]}\n"
        return pair
    
    def show_message_box(self, msg):
        message_box = QMessageBox()
        message_box.setText(msg)
        message_box.exec_()
        # Close the message box after 2 seconds
        QTimer.singleShot(2000, lambda: message_box.done(QMessageBox.Ok))