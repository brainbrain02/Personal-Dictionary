from PyQt5 import uic
from PyQt5.QtWidgets import *
from constant import *
import random

class First(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('first.ui', self)

        ### Main function setup
        self.func = MainFunction()
        # Open current dictionary
        current_word = self.func.read_word()
        if current_word:
            self.update_mean_text(current_word)
        else:
            message = QMessageBox()
            message.setText("Can not read the current dictionary!")
            message.exec_()

        # Check answer box is empty
        self.enter_btn.clicked.connect(lambda: self.handle_ans_enter(self.ans_entry.text()))
    
    def update_mean_text(self, text):
        self.mean_lab2.setText(text) 

    def handle_ans_enter(self, ans):
        word = self.func.check_answer_enterd(ans)
        if word:
            self.update_mean_text(f"Wrong Answer!\nThe answer should be: {word}\n")

class MainFunction():
    def check_answer_enterd(self, ans):
        if ans != "":
            return self.check_ans_correct(ans)
        else:
            message = QMessageBox()
            message.setText("Please enter an answer!")
            message.exec_()
            return

    def read_word(self):
        try:
            with open(current_dict_path, 'r') as file:
                contents = file.readlines()
                self.random_line = random.choice(contents)
                text = self.random_line.rstrip('\n')
                self.current_pair = text.split(':')
                return f"{self.current_pair[1]}"
        except FileNotFoundError:
            print(f"File not found: {current_dict_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def check_ans_correct(self, answer):
        ans = answer.lower()
        if ans != self.current_pair[0]:
            with open(wrong_word_path, 'a') as wrong_file:
                wrong_file.writelines(f"{self.random_line}\n")
            return self.current_pair[0]
        else:
            with open(correct_word_path, 'a') as correct_file:
                correct_file.write(f"{self.random_line}\n")
            return