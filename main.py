# GUI to open file browser to locate and import and save json files
# Allow user to interact with GUI to edit and save values
# Written by Steve Michel

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import os
import json
import shutil

# Hard paths to gui
# gui_use = "my_gui_01.ui"
# import the ui file - added this path reference to allow
ui_file = os.path.join(os.path.dirname(__file__), 'my_gui_01.ui')


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(ui_file, self)
        self.directory_path_use = os.path.dirname(os.path.abspath(__file__))
        self.json_data = None
        self.raw_data_from_json = None
        self.new_filename = None
        self.number_records = None
        self.create_new_record = None
        self.filename_without_ext = None
        self.temp_filename_for_new_record = None
        self.browse.clicked.connect(self.file_browse)
        self.recordChange_name.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9\\s]+"), self))
        self.recordChange_age.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self))
        self.recordChange_gender.addItems([""])
        self.recordChange_shirtSize.addItems([""])
        self.recordChange_pantSize.addItems([""])
        self.recordChange_shoeSize.addItems([""])
        self.recordChange_isAvail.addItems([""])
        self.recordChange_notes.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9.,<>+*\\s]+"), self))
        self.textBrowser_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9_\\- ]+"), self))
        self.SaveRecord.clicked.connect(self.save_record_changes)
        self.textBrowser_3.textChanged.connect(self.update_text_browser_5)
        self.SaveRecord.setEnabled(False)
        self.path_use = None

    def file_browse(self):
        # Browse to File
        json_name = QFileDialog.getOpenFileName(self, "Open file", self.directory_path_use, "JSON files (*.json)")

        if json_name[0]:
            # Display full path of selected JSON file
            self.filenameDisplay.setText(json_name[0])
            # grab path and save
            self.path_use = os.path.dirname(json_name[0])
            # print(self.directory_path_use)
            # print(self.path_use)
            # grab and display name of selected JSON file
            filename_use = os.path.basename(json_name[0])
            self.textBrowser_2.setText(filename_use)
            # strip extension (hack) then add _new and display
            self.filename_without_ext = os.path.splitext(filename_use)[0]
            new_filename_temp = self.filename_without_ext + "_update"
            # textBrowser_3 is an editable field allowing user to create new base file name
            self.textBrowser_3.setText(new_filename_temp)
            # create new filename by adding .json
            self.new_filename = new_filename_temp + ".json"

            # JSON exception handling
            try:
                self.open_json_file(json_name[0])
                self.set_combobox()
                self.create_table_widget()
                self.comboBox_SelectRecord.currentIndexChanged.connect(self.record_edit)
            except json.decoder.JSONDecodeError:
                self.display_json_error()

    def open_json_file(self, json_path):
        # open the json file
        with open(json_path, 'r') as file:
            json_data = file.read()
        # store raw json data into dictionary
        self.raw_data_from_json = json.loads(json_data)
        # determine number of records in dictionary
        self.number_records = len((self.raw_data_from_json["actors"]))
        self.textBrowser_4.setText(str(self.number_records))

    def set_combobox(self):
        # This combobox allows the user to select which record to edit
        # clear combobox so that it appears blank until there is a record
        self.comboBox_SelectRecord.clear()
        # create the range of choices. "None" will clear the selection. "Create" will allow for new record
        self.comboBox_SelectRecord.addItem("None")
        self.comboBox_SelectRecord.setCurrentIndex(-1)
        for i in range(1, self.number_records + 1):
            self.comboBox_SelectRecord.addItem(str(i))
        self.comboBox_SelectRecord.addItem("Create")

    def create_table_widget(self):
        # this table widget will display the parsed JSON data
        # the keys list will produce the headers
        keys_list = list(self.raw_data_from_json["actors"][0].keys())
        # row count is set by the number of records
        self.tableWidget.setRowCount(self.number_records)
        # column count is set by number of keys
        self.tableWidget.setColumnCount(len(keys_list))
        # header labels come from keys_list
        self.tableWidget.setHorizontalHeaderLabels(keys_list)
        rows = []
        # rows becomes a list of lists, a list of values_list
        for actor in range(self.number_records):
            # each values_list is populated by the values of each actor's dictionary
            values_list = list(self.raw_data_from_json["actors"][actor].values())
            rows.append(values_list)
        # iterates thru rows to populate the tableWidget
        for row_idx, row_data in enumerate(rows):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                # this flag allows table to update after user edit
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row_idx, col_idx, item)
        self.tableWidget.resizeColumnsToContents()

    def display_json_error(self):
        # Error message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("The selected file is not a valid JSON file. Please select a different file.")
        msg.setWindowTitle("JSON Error")
        msg.exec_()
        self.file_browse()

    def update_text_browser_5(self):
        # this creates and displays the filename that will be saved
        new_filename_temp = os.path.splitext(self.textBrowser_3.text())[0]
        self.new_filename = new_filename_temp + ".json"
        self.textBrowser_5.setText(self.new_filename)

    def record_edit(self, index):
        # when self.create_new_record is True, additional records are appended to the dictionary
        # This value needs to be False when editing existing records
        self.create_new_record = False

        # the index is the value the user selected from the combobox
        # These values will clear the editing boxes
        if index < 0:
            self.recordChange_name.setText("")
            self.recordChange_age.setText("")
            self.recordChange_gender.setCurrentIndex(-1)
            self.recordChange_shirtSize.setCurrentIndex(-1)
            self.recordChange_pantSize.setCurrentIndex(-1)
            self.recordChange_shoeSize.setCurrentIndex(-1)
            self.recordChange_isAvail.setCurrentIndex(-1)
            self.recordChange_notes.setText("")
            return

        # Create List of Shoe Sizes from 4 to 16 in 0.5 increment
        shoe_size_vals = []
        for size in range(8, 33):
            shoe_size_vals.append(str(size / 2))

        # set table_index to 1 less than index as zero_index compensation
        table_index = index - 1
        # populate these variables with values from the table
        # these values will populate the edit boxes
        selected_record_data = self.tableWidget.item(table_index, 0)
        selected_record_age = self.tableWidget.item(table_index, 1)
        selected_record_gender = self.tableWidget.item(table_index, 2)
        selected_record_shirt_size = self.tableWidget.item(table_index, 3)
        selected_record_pant_size = self.tableWidget.item(table_index, 4)
        selected_record_shoe_size = self.tableWidget.item(table_index, 5)
        selected_record_is_avail = self.tableWidget.item(table_index, 6)
        selected_record_notes = self.tableWidget.item(table_index, 7)

        # if user selects "create" then the index is greater than number of records
        # As there is no existing data in a new record, we will populate the
        # variables with another record to get the correct data type

        if index > self.number_records:
            # set table_index to 1 less than index as zero_index compensation
            table_index = self.number_records - 1
            selected_record_data = self.tableWidget.item(table_index, 0)
            selected_record_age = self.tableWidget.item(table_index, 1)
            selected_record_gender = self.tableWidget.item(table_index, 2)
            selected_record_shirt_size = self.tableWidget.item(table_index, 3)
            selected_record_pant_size = self.tableWidget.item(table_index, 4)
            selected_record_shoe_size = self.tableWidget.item(table_index, 5)
            selected_record_is_avail = self.tableWidget.item(table_index, 6)
            selected_record_notes = self.tableWidget.item(table_index, 7)
            # change the create_new_record to True to allow dictionary to append
            self.create_new_record = True

        # if there are values in the editable fields, populate the boxes
        if selected_record_data is not None:
            # once there are values in the boxes, the save button is enabled
            self.SaveRecord.setEnabled(True)
            # fill in the name data
            self.recordChange_name.setText(selected_record_data.text())
            # if it is a new record, fill in with "New"
            if self.create_new_record:
                self.recordChange_name.setText("New")
            # fill in age , or if new record set text to "0"
            self.recordChange_age.setText(selected_record_age.text())
            if self.create_new_record:
                self.recordChange_age.setText("0")
            # allow user to select gender
            self.recordChange_gender.clear()
            self.recordChange_gender.addItems(["Female", "Male", "Non-binary", "Trans"])
            gender_options = ["Female", "Male", "Non-binary", "Trans"]
            gender_value = selected_record_gender.text()
            gender_index = gender_options.index(gender_value)
            gender_index_use = gender_index
            self.recordChange_gender.setCurrentIndex(gender_index_use)
            if self.create_new_record:
                self.recordChange_gender.setCurrentIndex(0)
            # allow user to select shirt size
            self.recordChange_shirtSize.clear()
            self.recordChange_shirtSize.addItems(["XS", "S", "M", "L", "XL"])
            shirt_options = ["XS", "S", "M", "L", "XL"]
            shirt_values = selected_record_shirt_size.text()
            shirt_index = shirt_options.index(shirt_values)
            shirt_index_use = shirt_index
            self.recordChange_shirtSize.setCurrentIndex(shirt_index_use)
            if self.create_new_record:
                self.recordChange_shirtSize.setCurrentIndex(0)
            # Allow user to select pant size
            self.recordChange_pantSize.clear()
            self.recordChange_pantSize.addItems(["XS", "S", "M", "L", "XL"])
            pant_options = ["XS", "S", "M", "L", "XL"]
            pant_values = selected_record_pant_size.text()
            pant_index = pant_options.index(pant_values)
            pant_index_use = pant_index
            self.recordChange_pantSize.setCurrentIndex(pant_index_use)
            if self.create_new_record:
                self.recordChange_pantSize.setCurrentIndex(0)
            # Allow user to select shoe size
            self.recordChange_shoeSize.clear()
            self.recordChange_shoeSize.addItems(shoe_size_vals)
            shoe_options = shoe_size_vals
            selected_record_shoe_size_temp = float(selected_record_shoe_size.text())
            shoe_values = str(selected_record_shoe_size_temp)
            shoe_index = shoe_options.index(shoe_values)
            shoe_index_use = shoe_index
            self.recordChange_shoeSize.setCurrentIndex(shoe_index_use)
            if self.create_new_record:
                self.recordChange_shoeSize.setCurrentIndex(0)
            # allow user to ender True or False - boolean handling happens later
            self.recordChange_isAvail.clear()
            self.recordChange_isAvail.addItems(["True", "False"])
            avail_options = (["True", "False"])
            avail_values = selected_record_is_avail.text()
            avail_index = avail_options.index(avail_values)
            avail_index_use = avail_index
            self.recordChange_isAvail.setCurrentIndex(avail_index_use)
            if self.create_new_record:
                self.recordChange_isAvail.setCurrentIndex(0)
            # Allow user to enter notes
            self.recordChange_notes.setText(selected_record_notes.text())
            if self.create_new_record:
                self.recordChange_notes.setText("")

        else:
            # This block clears all the values from the edit boxes and dis-ables the save button
            self.SaveRecord.setEnabled(False)
            self.recordChange_name.setText("")
            self.recordChange_age.setText("")
            self.recordChange_gender.clear()
            self.recordChange_shirtSize.clear()
            self.recordChange_pantSize.clear()
            self.recordChange_shoeSize.clear()
            self.recordChange_isAvail.clear()
            self.recordChange_notes.setText("")

    def save_record_changes(self):
        # create a condition for writing the record later
        write_the_record = False
        # index val gets the value of the comboBox
        index_val = self.comboBox_SelectRecord.currentIndex()
        if index_val < 0:
            return

        # set table_index to 1 less than index as zero_index compensation
        table_index = index_val - 1

        # Get the new values from the user inputs
        name = self.recordChange_name.text()
        age = self.recordChange_age.text()
        gender = self.recordChange_gender.currentText()
        shirt_size = self.recordChange_shirtSize.currentText()
        pant_size = self.recordChange_pantSize.currentText()
        shoe_size = self.recordChange_shoeSize.currentText()
        is_avail = self.recordChange_isAvail.currentText()
        notes = self.recordChange_notes.text()

        # convert string "True" and "False" to boolean
        bool_builder = ""
        if is_avail == "True":
            bool_builder = "True"
        bool_is_avail = bool(bool_builder)

        # if we aren't adding a new record, then we are updating an existing record
        if not self.create_new_record:
            # Update the corresponding values in the JSON data
            # the table_index sets the "actor" to update
            self.raw_data_from_json["actors"][table_index]["name"] = name
            self.raw_data_from_json["actors"][table_index]["age"] = int(age)
            self.raw_data_from_json["actors"][table_index]["gender"] = gender
            self.raw_data_from_json["actors"][table_index]["shirtSize"] = shirt_size
            self.raw_data_from_json["actors"][table_index]["pantSize"] = pant_size
            self.raw_data_from_json["actors"][table_index]["shoeSize"] = float(shoe_size)
            self.raw_data_from_json["actors"][table_index]["isAvailable"] = bool_is_avail
            self.raw_data_from_json["actors"][table_index]["notes"] = notes

            # create condition for whether file was written
            file_written = False

            write_file_name = os.path.join(self.path_use, self.new_filename)

            while os.path.isfile(write_file_name):
                file_dialog = QFileDialog()
                # if the file exists, open a file dialog to allow the user to select a new filename
                popup_message = f"You are here because {write_file_name} already exists"
                new_filename_temp, _ = file_dialog.getSaveFileName(None, popup_message, write_file_name,
                                                                   "JSON Files (*.json)")
                if not new_filename_temp:  # if user clicks cancel, exits check and won't save the record
                    break
                # Write the updated JSON data to the file
                with open(new_filename_temp, 'w') as file:
                    json.dump(self.raw_data_from_json, file, indent=4)
                    write_file_name_temp = os.path.basename(new_filename_temp)  # Update the new filename
                    write_file_name = os.path.join(self.path_use, write_file_name_temp)
                    # print(write_file_name)
                    if os.path.isfile(write_file_name):
                        file_written = True
                    break

            # checks to see if write_file_name does NOT exist and then saves it
            if not os.path.isfile(write_file_name):
                # print(f"{write_file_name} isn't there, so we are writing it")
                with open(write_file_name, 'w') as file:
                    json.dump(self.raw_data_from_json, file, indent=4)
                    if os.path.isfile(write_file_name):
                        file_written = True

            # Update the table widget with the new values
            # the table_index sets the row or "actor" to update
            # this block is here now, the table VIEW gets updated only if the record gets written
            if file_written:
                self.tableWidget.setItem(table_index, 0, QTableWidgetItem(name))
                self.tableWidget.setItem(table_index, 1, QTableWidgetItem(age))
                self.tableWidget.setItem(table_index, 2, QTableWidgetItem(gender))
                self.tableWidget.setItem(table_index, 3, QTableWidgetItem(shirt_size))
                self.tableWidget.setItem(table_index, 4, QTableWidgetItem(pant_size))
                self.tableWidget.setItem(table_index, 5, QTableWidgetItem(shoe_size))
                self.tableWidget.setItem(table_index, 6, QTableWidgetItem(is_avail))
                self.tableWidget.setItem(table_index, 7, QTableWidgetItem(notes))

            # resets the combobox to clear the values
            self.comboBox_SelectRecord.setCurrentIndex(-1)

        # if create_new_record is "True" then we need to make a new record to append
        if self.create_new_record:
            # first make a new dictionary
            my_dict = {
                'name': self.recordChange_name.text(),
                'age': int(self.recordChange_age.text()),
                'gender': self.recordChange_gender.currentText(),
                'shirt_size': self.recordChange_shirtSize.currentText(),
                'pant_size': self.recordChange_pantSize.currentText(),
                'shoe_size': float(self.recordChange_shoeSize.currentText()),
                'is_avail': bool_is_avail,
                'notes': self.recordChange_notes.text()
            }

            # Append my_dict to the JSON data
            self.raw_data_from_json['actors'].append({
                'name': my_dict['name'],
                'age': my_dict['age'],
                'gender': my_dict['gender'],
                'shirtSize': my_dict['shirt_size'].upper(),
                'pantSize': my_dict['pant_size'].upper(),
                'shoeSize': my_dict['shoe_size'],
                'isAvailable': my_dict['is_avail'],
                'notes': my_dict['notes']
            })

            # Write the NEW JSON data to a temp folder
            # print(self.filename_without_ext)
            self.temp_filename_for_new_record = self.filename_without_ext + "_new_tmp.json"
            path_use_to_temp = os.path.join(self.directory_path_use, "temp")
            path_use_to_temp_with_file = os.path.join(path_use_to_temp, self.temp_filename_for_new_record)
            # print(path_use_to_temp_with_file)
            destination_path = os.path.join(self.path_use, self.new_filename)
            # print(destination_path)

            # with open(self.temp_filename_for_new_record, 'w') as file:
            #     json.dump(self.raw_data_from_json, file, indent=4)
            with open(path_use_to_temp_with_file, 'w') as file:
                json.dump(self.raw_data_from_json, file, indent=4)

            # Open a dialog box to ask the user if they want to continue adding records or go back to editing records
            this_message = f"{self.temp_filename_for_new_record} saved successfully. What would you like to do next?"
            dialog = QMessageBox()
            dialog.setWindowTitle("Record Changes Saved")
            dialog.setText(this_message)
            dialog.addButton("Continue Adding Records", QMessageBox.AcceptRole)
            dialog.addButton("Go Back to Editing Records", QMessageBox.RejectRole)
            response = dialog.exec_()

            # Handle the user's response
            if response == QMessageBox.AcceptRole:
                # Continue adding records
                # reset comboBox to clear the data
                self.comboBox_SelectRecord.setCurrentIndex(-1)
                # reset comboBox to "Create"" to populate the data
                self.comboBox_SelectRecord.setCurrentIndex(self.number_records + 1)
                pass
            elif response == QMessageBox.RejectRole:
                # copy temp file to updated record file
                destination_path = os.path.join(self.path_use, self.new_filename)
                write_the_record = True
                pass

            if write_the_record:
                # print(f"Source full file and path {path_use_to_temp_with_file}")
                # print(f"Destination file and path {destination_path}")

                if os.path.exists(destination_path):
                    destination_path_temp, _ = QFileDialog.getSaveFileName(None, "Save As", self.path_use,
                                                                           "JSON Files (*.json)")
                    # print(destination_path_temp)
                    destination_path = os.path.join(path_use_to_temp, destination_path_temp)

                # print(destination_path)
                # Copy the file to the destination
                try:
                    shutil.copy(path_use_to_temp_with_file, destination_path)
                    # delete the source file
                    os.remove(path_use_to_temp_with_file)
                except shutil.Error as e:
                    print(f"Error copying file: {e}")
                except Exception as e:
                    print(f"Error: {e}")
                # resets the combobox to clear the values
                self.comboBox_SelectRecord.setCurrentIndex(-1)


app = QApplication(sys.argv)
main_window = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(main_window)
widget.setFixedWidth(900)
widget.setFixedHeight(500)
widget.show()
sys.exit(app.exec_())
