from PyQt5 import uic
from PyQt5.QtWidgets import *
from first import First, MainFunction
from second import Second
from constant import *

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
        

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()