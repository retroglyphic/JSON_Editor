This JSON_Editor was written in Python 3.7 using PyCharm

=====================
=====================

List of import statements:

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import os
import json
import shutil

=====================
=====================

To work with the JSON_Editor, note that any text-field or button that has an underlined label is editable or clickable.


To begin, use the <Browse> button to locate and load a json file.

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
None
1
2
3
4
5
6
Create

If a user selects a number, the record associated with that table-index will be displayed in the value editing boxes.

If a user selects None, then it will clear any values displayed in the editing boxes.

If a user selects Create, then the user can create a record for a new actor.

==========================================

Value editing boxes

These text entry boxes are QLineEdit boxes
Name
Age
Notes

These "choice" boxes are QCombo boxes
Gender
ShirtSize
PantSize
ShoesSize
IsAvailable

Once there are values in the editing boxes, then the <Save Record> button is enabled.

==========================================

<Save Record> 

When the user clicks <Save Record> :
The record will be saved to a new json file with the name shown in the New File Name box. 
The values in the table will be updated.

If the user has created a new record, this record does get saved. However, the new record is not visible in the table until the new json file gets loaded and parsed.

It is possible to create many new records

=====================

Future goals:
-rework the table view to allow the viewing of new records
-allow user to select alternate css or layouts
-include a record <Delete> function with a "are you sure" check





