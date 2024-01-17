from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Third(QWidget):
    def __init__(self, storage):
        super().__init__()
        uic.loadUi('third.ui', self)
        self.display.setColumnWidth(0, 200)
        self.display.setColumnWidth(1, 500)
        self.display.setColumnWidth(2, 59)
        
        ### Main function setup
        self.storage = storage

        # self.populate_tree(self.display, self.storage.dict, self.storage.state)
        self.populate_tree(self.display, self.storage.dictionary)
        self.display.itemClicked.connect(self.display_popup)
        self.config_btn.clicked.connect(self.ask_new_repetition)
        
    def add_tree_item(self, parent_text, item_data):
        parent_item = self.find_tree_item(parent_text)
        if parent_item is not None:
            child_item = QTreeWidgetItem(parent_item, item_data)
            return child_item
    
    def populate_tree(self, tree_widget, data):
        for word, attributes in data.items():
            row = QTreeWidgetItem(tree_widget)
            row.setText(0, word)
            row.setText(1, attributes.get("definition"))
            checkbox = QCheckBox()
            tree_widget.setItemWidget(row, 2, checkbox)
            if attributes.get("state"):
                checkbox.setChecked(True)
            checkbox.clicked.connect(lambda state, key=word: 
                                     self.checkbox_state_changed(state, key))


    def checkbox_state_changed(self, state, key):
        sender_checkbox = self.sender()
        item = self.display.itemAt(sender_checkbox.pos())
        if item is not None:
            # Use assignment, not equality check
            if not state and len(self.storage.current_dict) == 1:
                message = QMessageBox()
                message.setText("The testing flash card database must have at least 1 word!")
                message.exec_()
                # Use setChecked to change the checkbox state
                sender_checkbox.setChecked(True)
                return
            # Update the state regardless of the condition
            self.storage.dictionary[key]["state"] = state
            # Update the current_dict based on the state
            if state and key not in self.storage.current_dict:
                self.storage.current_dict.append(key)
            elif not state and key in self.storage.current_dict:
                self.storage.current_dict.remove(key)

    def display_popup(self, item, column):
        pop = MyPopup(item.text(0), self.storage)
        pop.exec_()

    def ask_new_repetition(self):
        while True:
            number, ok = QInputDialog.getInt(None, "New space repetition number",
                                            "Please enter the new repetition you want.")
            if ok:
                if number > 0:
                    self.storage.config["word_repetition"] = number
                    break
                else:
                    QMessageBox.warning(None, "Invalid Input", "Please enter a positive integer.")
            else:
                break

class MyPopup(QDialog):
    def __init__(self, word, storage, parent=None):
        super().__init__(parent)
        self.storage = storage
        uic.loadUi('your_popup_ui.ui', self)  # Replace 'your_popup_ui.ui' with your actual UI file
        self.setWindowTitle('Popup Window')
        self.sound_btn.clicked.connect(lambda: self.storage.play_sound(self.storage.dictionary[word]["pronunciation"]))
        self.setup_ui(word)
        self.def_textbox.mousePressEvent = lambda event: self.reject()
        self.usage_textbox.mousePressEvent = lambda event: self.reject()
        self.example_textbox.mousePressEvent = lambda event: self.reject()
        self.mousePressEvent = lambda event: self.reject()

    def setup_ui(self, word):
        word_dict = self.storage.dictionary[word]
        self.word_lab2.setText(word)
        self.def_textbox.setText(word_dict["definition"])
        self.usage_textbox.setText(word_dict["usage"])
        self.example_textbox.setText(word_dict["example"])
        for i in range(4):
            if word_dict["common"][i]:
                self.common_box.addItem(self.storage.config["COMMOM_USAGE"][i])
        self.synonym_lab2.setText(word_dict["synonyms"][0])
        self.synonym_lab3.setText(word_dict["synonyms"][1])
        self.synonym_lab4.setText(word_dict["synonyms"][2])
        self.chinese_lab2.setText(word_dict["chinese"])
