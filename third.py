from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from constant import *

class Third(QWidget):
    def __init__(self, storage):
        super().__init__()
        uic.loadUi('third.ui', self)
        
        ### Main function setup
        self.storage = storage
        self.func = DictionaryFunction(self.storage)

        
    def add_tree_item(self, parent_text, item_data):
        parent_item = self.find_tree_item(parent_text)
        if parent_item is not None:
            child_item = QTreeWidgetItem(parent_item, item_data)
            return child_item

class DictionaryFunction():
    def __init__(self, storage):
        self.dict_list = storage.current_dict
        self.wrong_answer_list = storage.wrong_answer_list
        self.correct_answer_list = storage.correct_answer_list

    