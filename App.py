from PyQt5 import uic
from PyQt5.QtWidgets import *
from first import First
from second import Second
from third import Third
from constant import *
import json
from playsound import playsound
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create main window and pages
        uic.loadUi('pages.ui', self)
        self.storage = Storage()
        self.first = First(self.storage)
        self.stackedWidget.addWidget(self.first)
        self.first.change_btn.clicked.connect(self.go_to_second)
        self.second = Second(self.storage)
        self.stackedWidget.addWidget(self.second)
        self.second.change_btn.clicked.connect(self.go_to_third)
        self.third = Third(self.storage)
        self.stackedWidget.addWidget(self.third)
        self.third.change_btn.clicked.connect(self.go_to_first)

    def go_to_first(self):
        self.first.ans_entry.clear()
        current_word = self.first.func.choose_word(self.storage.current_dict)
        if current_word:
            self.first.update_word_information(current_word)
        else:
            message = QMessageBox()
            message.setText("Can not read the current dictionary!")
            message.exec_()
        self.stackedWidget.setCurrentIndex(0)

    def go_to_second(self):
        self.stackedWidget.setCurrentIndex(1)    

    def go_to_third(self):
        self.third.display.clear()
        self.third.populate_tree(self.third.display, self.storage.dictionary)
        self.stackedWidget.setCurrentIndex(2)    
    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Close Window', 'Are you sure you want to close the window?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.storage.write_json_file(config["dict_path"], self.storage.dictionary)
            self.storage.write_to_file(config["current_dict_path"], self.storage.current_dict)
            self.storage.write_to_file(config["wrong_word_path"], self.storage.wrong_answer_list)
            self.storage.write_to_file(config["correct_word_path"], self.storage.correct_answer_list)
            event.accept()
        else:
            event.ignore()

class Storage():
    # Create current_dict, correct_word, wrong_word here
    def __init__(self) -> None:
        self.dictionary = {}
        self.current_dict = []
        self.wrong_answer_list = []
        self.correct_answer_list = []
        self.dictionary = self.read_json_file(config["dict_path"])
        self.current_dict = self.read_file(
            config["current_dict_path"])
        self.wrong_answer_list = self.read_file(
            config["wrong_word_path"])
        self.correct_answer_list = self.read_file(
            config["correct_word_path"])
        if not self.current_dict:
            self.handle_empty_dict(self.dictionary)

    def read_json_file(self, path):
        with open(path, "r") as json_file:
            dictionary = json.load(json_file)
        return dictionary

    def write_json_file(self, path, dict):
        with open(path, "w") as json_file:
            json.dump(dict, json_file, indent=2)

    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                word_list = [line.strip() for line in file]
        except FileNotFoundError:
            path = config["current_dict_path"]
            print(f"File not found: {path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return word_list

    def write_to_file(self, path, list):
        with open(path, 'w') as file:
            for line in list:
                file.write(line + '\n')

    def handle_empty_dict(self, dict):
        if not self.current_dict:
            if not self.correct_answer_list and not self.wrong_answer_list:
                self.current_dict = list(dict.keys())
                self.handle_word_state(self.current_dict, self.dictionary)
            elif not self.correct_answer_list and self.wrong_answer_list:
                self.current_dict = self.wrong_answer_list[:]
                self.wrong_answer_list = []

    def handle_word_state(self, current_dict, dict):
        for word, att in dict.items():
            if not att["state"]:
                current_dict.remove(word)

    def convert_readable_common(self, list):
        common = []
        if list[0]:
            common.append("Formal")
        if list[1]:
            common.append("Informal")
        if list[2]:
            common.append("Written")
        if list[3]:
            common.append("Spoken")
        common_str = ", ".join(common)
        common_sen = f"{common_str} English"
        return common_sen

    def play_sound(self, path):
        playsound(path)
    

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()