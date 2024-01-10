from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from first import First, FlashCardFunction
from second import Second
from constant import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create main window and pages
        uic.loadUi('pages.ui', self)
        self.first = First()
        self.stackedWidget.addWidget(self.first)
        self.first.change_btn.clicked.connect(self.go_to_second)
        self.second = Second()
        self.stackedWidget.addWidget(self.second)
        self.second.change_btn.clicked.connect(self.go_to_first)

    def go_to_first(self):
        self.stackedWidget.setCurrentIndex(0)

    def go_to_second(self):
        self.stackedWidget.setCurrentIndex(1)    
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Close Window', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.first.func.overwrite_current_dict(current_dict_path, self.first.func.dict_list)
            self.first.func.write_to_file(wrong_word_path, self.first.func.wrong_list)
            self.first.func.write_to_file(correct_word_path, self.first.func.correct_list)
            event.accept()
        else:
            event.ignore()
        
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()