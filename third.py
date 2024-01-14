from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from constant import *

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
        # Check if the clicked column is the second column (index 1)
        if column == 1:
            # Get the text from the second column
            value_list = []
            synonyms_list = []
            word_dict = self.storage.dictionary[item.text(0)]

            for key, value in word_dict.items():
                synonyms_list = []
                if value and key != "state" and key != "add time" and key != "test time":  # change this line when adding the timestamp feature
                    if key == "synonyms":
                        for synonym in value:
                            synonyms_list.append(synonym)
                        synonyms = "<br>".join(synonyms_list)
                        value_list.append(f"<b>{key.title()}:</b><br>{synonyms}<br>")
                    else:
                        value_list.append(f"<b>{key.title()}:</b><br>{value}<br><br>")

            value_text = "".join(value_list)

            # Create a window
            popup_dialog = QDialog()
            text_edit = QTextEdit()
            text_edit.setHtml(value_text)
            font = text_edit.font()
            font.setPointSize(13)
            text_edit.setFont(font)
            text_edit.setFixedSize(550, 600)
            layout = QVBoxLayout(popup_dialog)
            layout.addWidget(text_edit)
            popup_dialog.setLayout(layout)
            text_edit.mousePressEvent = lambda event: popup_dialog.reject()
            popup_dialog.exec_()