from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime

class Third(QWidget):
    def __init__(self, storage):
        super().__init__()
        uic.loadUi('third.ui', self)
        self.display.setColumnWidth(0, 190)
        self.display.setColumnWidth(1, 490)
        self.display.setColumnWidth(2, 59)
        
        ### Main function setup
        self.storage = storage

        # self.populate_tree(self.display, self.storage.dict, self.storage.state)
        self.populate_tree(self.display, self.storage.dictionary)
        self.display.itemClicked.connect(self.display_popup)
        self.config_btn.clicked.connect(self.ask_new_repetition)
        self.check_all_btn.clicked.connect(self.tick_all_checkbox)
        self.search_bar.textChanged.connect(self.filter_tree)
        self.check_date_btn.clicked.connect(self.tick_checkbox_after)
        
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
        total = len(self.storage.current_dict) + len(self.storage.correct_answer_list) \
                + len(self.storage.wrong_answer_list)
        if item is not None:
            # Use assignment, not equality check
            if not state and total == 1:
                message = QMessageBox()
                message.setText("The testing flash card database must have at least 1 word!")
                message.exec_()
                # Use setChecked to change the checkbox state
                sender_checkbox.setChecked(True)
                return
            self.change_word_state(key, state)
            
    
    def change_word_state(self, word, state):
        # Update the state regardless of the condition
        self.storage.dictionary[word]["state"] = state
        # Update the current_dict based on the state
        if state and word not in self.storage.current_dict:
            self.storage.current_dict.append(word)
        elif not state and word in self.storage.current_dict:
            self.storage.current_dict.remove(word)
        elif not state and word in self.storage.wrong_answer_list:
            self.storage.wrong_answer_list.remove(word)
        elif not state and word in self.storage.correct_answer_list:
            self.storage.correct_answer_list.remove(word)
        self.storage.handle_empty_dict(self.storage.dictionary)


    def display_popup(self, item, column):
        if column == 1:
            pop = MyPopup(item.text(0), self.storage)
            pop.exec_()

    def ask_new_repetition(self):
        while True:
            current = self.storage.config["word_repetition"]
            number, ok = QInputDialog.getInt(None, "New space repetition number",
                                            f"The current repetition is {current}\nPlease enter the new repetition you want.")
            if ok:
                if number > 0:
                    self.storage.config["word_repetition"] = number
                    break
                else:
                    QMessageBox.warning(None, "Invalid Input", "Please enter a positive integer.")
            else:
                break
    
    def tick_all_checkbox(self):
        for top_level_item_index in range(self.display.topLevelItemCount()):
            top_level_item = self.display.topLevelItem(top_level_item_index)
            # Assuming checkbox is in the third column (column index 2)
            checkbox = self.display.itemWidget(top_level_item, 2)
            if checkbox and isinstance(checkbox, QCheckBox):
                checkbox.setChecked(True)
                self.change_word_state(top_level_item.text(0), 1)
            else:
                print(f"No valid checkbox found for top-level item {top_level_item_index}")
    
    def tick_checkbox_after(self):
        dialog = CalendarDialog(self.storage)
        dialog.exec_()
        dates = dialog.get_dates()
        if dates:
            for index in range(self.display.topLevelItemCount()):
                item = self.display.topLevelItem(index)
                word = item.text(0)
                checkbox = self.display.itemWidget(item, 2)
                if word in dates:
                # Assuming checkbox is in the third column (column index 2)
                    if isinstance(checkbox, QCheckBox):
                        checkbox.setChecked(True)
                        self.change_word_state(item.text(0), 1)
                else:
                    if isinstance(checkbox, QCheckBox):
                        checkbox.setChecked(False)
                        self.change_word_state(item.text(0), 0)

        

    def filter_tree(self):
        search_text = self.search_bar.text().lower()
        for i in range(self.display.topLevelItemCount()):
            item = self.display.topLevelItem(i)
            word = item.text(0).lower()
            item.setHidden(search_text not in word)
        
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
        self.synonym_lab2.setText(word_dict["synonyms"][0].title())
        self.synonym_lab3.setText(word_dict["synonyms"][1].title())
        self.synonym_lab4.setText(word_dict["synonyms"][2].title())
        self.chinese_lab2.setText(word_dict["chinese"])

class CalendarDialog(QDialog):
    def __init__(self, storage):
        super().__init__()
        # Load the UI file
        uic.loadUi('calendar.ui', self)
        self.storage = storage
        self.dates = []
        # Connect the selectionChanged signal to the on_date_selected slot
        self.calendar.selectionChanged.connect(self.on_date_selected)

    def on_date_selected(self):
        selected_date = self.calendar.selectedDate()
        date = selected_date.toString('yyyy-MM-dd')
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        self.dates = self.find_word(self.date)
        self.accept()

    def find_word(self, target):
        dates = []
        for word, detail in self.storage.dictionary.items():
            date = datetime.strptime(detail["add time"], "%Y-%m-%d").date()
            if target < date:
                dates.append(word)
        return dates
    
    def get_dates(self):
        if self.dates:
            return self.dates
        return
