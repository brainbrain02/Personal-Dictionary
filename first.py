from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from constant import *
import random
import sys

class First(QWidget):
    def __init__(self, storage):
        super().__init__()
        uic.loadUi('first.ui', self)

        ### Main function setup
        self.storage = storage
        self.func = FlashCardFunction(self.storage)
        # Open current dictionary
        # current_word = self.func.read_current_dict()
        current_word = self.func.choose_word(self.storage.current_dict)
        if current_word:
            self.update_mean_text(current_word[1])
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

    def update_mean_text(self, text):
        self.mean_lab2.setText(text) 

    def handle_ans_enter(self, ans):
        # Check answer entered
        if not self.func.check_answer_enterd(ans):
            # Check answer correctness
            word = self.func.check_ans_correct(ans)
            if word:
                self.update_mean_text(
                    f"Wrong Answer!\nThe answer should be: {word}\n"
                    )
                loop = QEventLoop()
                QTimer.singleShot(2000, loop.quit)
                loop.exec_()
            # Generating next word
            # should I cross over the function parameter 
            # and directly control the upper layer object?
            self.ans_entry.clear()
            self.func.dict_list.remove(self.func.random_line)
            self.func.handle_empty_dict()
            next_word = self.func.choose_word(self.func.dict_list)
            if next_word:
                self.update_mean_text(next_word[1])
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
        # self.wrong_list = []
        # self.correct_list = []
        # self.dict_list = []
        self.dict_list = storage.current_dict
        self.wrong_list = storage.wrong_answer_list
        self.correct_list = storage.correct_answer_list

    def check_answer_enterd(self, ans):
        if not ans:
            message = QMessageBox()
            message.setText("Please enter an answer!")
            message.exec_()
            return True

    def read_current_dict(self):
        try:
            with open(current_dict_path, 'r') as file:
                self.dict_list = file.readlines()
                return f"{self.choose_word(self.dict_list)[1]}"
        except FileNotFoundError:
            print(f"File not found: {current_dict_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def choose_word(self, dict_list):
        self.random_line = random.choice(dict_list)
        text = self.random_line.rstrip('\n')
        self.current_pair = text.split(':')
        return self.current_pair

    def check_ans_correct(self, answer):
        ans = answer.lower()
        if ans != self.current_pair[0]:
            pair = self.form_pair(self.current_pair)
            self.wrong_list.append(pair)
            return self.current_pair[0]
        else:
            pair = self.form_pair(self.current_pair)
            self.correct_list.append(pair)
            return
    
    def form_pair(self, list):
        pair = f"{list[0]}:{list[1]}\n"
        return pair

    def write_to_file(self, path, list):
        with open(path, 'w') as file:
            for pair in list:
                file.writelines(f"{pair}\n")
    
    def overwrite_current_dict(self, path, list):
        with open(path, 'w') as file:
            for line in list:
                file.writelines(line)

    def handle_empty_dict(self):
        if not self.dict_list:
            if not self.correct_list:
                message = QMessageBox()
                message.setText("Well, you got none of them correct!\
                                \nCan't help you!")
                message.exec_()
            self.dict_list = self.correct_list[:]
            self.correct_list = []