# JSON_Editor
Allows user to view, edit, append and save specific json files

This JSON_Editor was written in Python 3.7 using PyCharm
=====================
=====================

Be sure to run the main.py from within the JSON_Editor directory. 

Be sure that the JSON_Editor directory contains these 2 files:
-  main.py
-  my_gui_01.ui

Be sure that the JSON_Editor directory contains these 2 folders:
-  /json_files
-  /temp

=====================
=====================

List of import statements:

- import sys
- from PyQt5 import QtWidgets, QtCore, QtGui
- from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QTableWidgetItem, QMessageBox
- from PyQt5.uic import loadUi
- import os
- import json
- import shutil

=====================
=====================

To work with the JSON_Editor, note that any text-field or button that has an underlined label is editable or clickable.


To begin, use the "Browse" button to locate and load a json file.

Once a json file is loaded the user can:
- see full path to the selected file.
- see base source file name.
- view and EDIT the suggested name in the Suggested New File Name field.
- see parsed records in the viewing table. 
- use the comboBox next to "Select Record to Edit"

==========================================

"Select Record to Edit" QComboBox usage

The choices are None, Numeric and Create. 
If there are 5 actors, the choices would look like this:
- None
- 1
- 2
- 3
- 4
- 5
- Create

If a user selects a number, the record associated with that table-index will be displayed in the value editing boxes.

If a user selects None, then it will clear any values displayed in the editing boxes.

If a user selects Create, then the user can create a record for a new actor.

==========================================

Value editing boxes

These text entry boxes are QLineEdit boxes:
- Name
- Age
- Notes

These "choice" boxes are QCombo boxes:
- Gender
- ShirtSize
- PantSize
- ShoesSize
- IsAvailable

Once there are values in the editing boxes, then the "Save Record" button is enabled.

==========================================

<Save Record> 

When the user clicks "Save Record" :

 - Existing Records:    The record will be saved to a new json file using the name shown in the New File Name box. 
The values in the table will be updated.

 - New Records:    If the user has created a new record, the new record is saved in a temp json file in the temp folder. That new file is then reloaded, reparsed and the values in the viewing table will be updated. Once user is done creating new records, the temp file is moved to the json_files folder, using the name shown in the New File Name box. It is possible to create many new records

=====================

Future goals:
- rework the table view to allow the viewing of new records - DONE
- allow user to select alternate css or layouts
- include a record <Delete> function with a "are you sure" check
