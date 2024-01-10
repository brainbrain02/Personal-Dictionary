from PyQt5 import uic
from PyQt5.QtWidgets import *
from first import First
from second import Second
from constant import *

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
        self.second.change_btn.clicked.connect(self.go_to_first)

    def go_to_first(self):
        self.stackedWidget.setCurrentIndex(0)

    def go_to_second(self):
        self.stackedWidget.setCurrentIndex(1)    
    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Close Window', 'Are you sure you want to close the window?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.storage.write_to_file(current_dict_path, self.storage.current_dict)
            self.storage.write_to_file(wrong_word_path, self.storage.wrong_answer_list)
            self.storage.write_to_file(correct_word_path, self.storage.correct_answer_list)
            print(self.storage.current_dict)
            print(self.storage.wrong_answer_list)
            print(self.storage.correct_answer_list)
            event.accept()
        else:
            event.ignore()

    
        
class Storage():
    # Create current_dict, correct_word, wrong_word here
    def __init__(self) -> None:
        self.current_dict = []
        self.wrong_answer_list = []
        self.correct_answer_list = []
        self.current_dict = self.read_file(
            current_dict_path, self.current_dict)
        self.wrong_answer_list = self.read_file(
            wrong_word_path, self.wrong_answer_list)
        self.correct_answer_list = self.read_file(
            correct_word_path, self.correct_answer_list)


    def read_file(self, file_path, pointer):
        try:
            with open(file_path, 'r') as file:
                pointer = file.readlines()
        except FileNotFoundError:
            print(f"File not found: {current_dict_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return pointer

    def write_to_file(self, path, list):
        with open(path, 'w') as file:
            for line in list:
                file.writelines(line)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()