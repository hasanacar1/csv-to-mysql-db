from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from create_table import create_table_page
from sql_workbench import sql_workbench_page

class import_csv_page(QWidget):
    def __init__(self, mydb, hostname, username, password, db_name):
        super().__init__()
        loadUi("import_csv.ui", self)
        self.setWindowTitle("Import CSV")
        self.mydb = mydb
        self.db_name = db_name
        self.hostname = hostname
        self.username = username
        self.password = password

        self.pushButton_load_data.setEnabled(False)
        self.pushButton_workbench.setEnabled(False)
        self.label_db_name.setText(db_name)
        self.pushButton_import_csv.clicked.connect(self.import_csv_func)
        self.pushButton_load_data.clicked.connect(self.load_data_func)
        self.pushButton_workbench.clicked.connect(self.sql_workbench_func)


    def import_csv_func(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file',
                                                'C:\\', "CSV File (*.csv)")
        if file_name[0] != '':
            self.csv_path = file_name[0]
            self.df_csv = pd.read_csv(self.csv_path, delimiter=";")
            print(self.df_csv.columns.to_list())
            model = pandasModel(self.df_csv)
            self.tableView_csv.setModel(model)
            self.pushButton_load_data.setEnabled(True)

    def load_data_func(self):
        #self.mydb, self.df_csv
        self.pushButton_workbench.setEnabled(True)
        self.pushButton_import_csv.setEnabled(False)
        self.create_table_obj = create_table_page(self.db_name, self.df_csv, self.hostname, self.username, self.password, self.csv_path)
        self.create_table_obj.show()
        self.create_table_obj.exec_()

    def sql_workbench_func(self):
        self.sql_workbench_obj = sql_workbench_page(self.db_name, self.df_csv, self.hostname, self.username, self.password)
        self.sql_workbench_obj.show()
        self.sql_workbench_obj.exec_()

class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
