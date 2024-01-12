from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from constant import *

class Third(QWidget):
    def __init__(self, storage):
        super().__init__()
        uic.loadUi('third.ui', self)
        self.display.setColumnWidth(0, 150)
        self.display.setColumnWidth(1, 410)
        self.display.setColumnWidth(2, 59)
        
        ### Main function setup
        self.storage = storage
        self.func = DictionaryFunction(self.storage)

        self.populate_tree(self.display, self.storage.dict, self.storage.state)
        self.display.itemClicked.connect(self.display_popup)
        
    def add_tree_item(self, parent_text, item_data):
        parent_item = self.find_tree_item(parent_text)
        if parent_item is not None:
            child_item = QTreeWidgetItem(parent_item, item_data)
            return child_item
    
    def populate_tree(self, tree_widget, data, state):
        for key, value in data.items():
            item = QTreeWidgetItem(tree_widget)
            item.setText(0, str(key))
            item.setText(1, str(value))
            checkbox = QCheckBox()
            tree_widget.setItemWidget(item, 2, checkbox)
            if state[key]:
                checkbox.setChecked(True)
            checkbox.clicked.connect(lambda state, key=key: self.checkbox_state_changed(state, key))

    def checkbox_state_changed(self, state, key):
        sender_checkbox = self.sender()
        item = self.display.itemAt(sender_checkbox.pos())
        if item is not None:
            # Use assignment, not equality check
            print(self.storage.current_dict)
            if not state and len(self.storage.current_dict) == 1:
                message = QMessageBox()
                message.setText("The testing flash card database must have at least 1 word!")
                message.exec_()
                # Use setChecked to change the checkbox state
                sender_checkbox.setChecked(True)
                return
            # Update the state regardless of the condition
            self.storage.state[key] = state == Qt.Checked
            # Update the current_dict based on the state
            if state and key not in self.storage.current_dict:
                self.storage.current_dict.append(key)
            elif not state and key in self.storage.current_dict:
                self.storage.current_dict.remove(key)

    def display_popup(self, item, column):
        # Check if the clicked column is the second column (index 1)
        if column == 1:
            # Get the text from the second column
            value_text = item.text(1)

            # Create a QLabel with the value text
            label = QLabel(value_text)

            # Create a QScrollArea to allow scrolling if content is too long
            scroll_area = QScrollArea(self)
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(label)

            # Set a fixed size for the pop-up window
            scroll_area.setMinimumSize(400, 300)

            # Create a QMessageBox to display the scroll area
            popup = QMessageBox(self)
            popup.setWindowTitle('Value')
            popup.layout().addWidget(scroll_area)

            # Show the popup
            popup.exec_()

class DictionaryFunction():
    def __init__(self, storage):
        self.storage = storage

    
    