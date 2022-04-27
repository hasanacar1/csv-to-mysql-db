from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
import mysql.connector
import csv

#, mydb, df_csv
class sql_workbench_page(QDialog):
    def __init__(self, db_name, df_csv, hostname, username, password):
        super().__init__()
        loadUi("sql_workbench.ui", self)
        self.setWindowTitle("SQL Workbench")
        self.df_csv = df_csv
        self.db_name = db_name
        self.hostname = hostname
        self.username = username
        self.password = password
        self.label_db_name.setText(db_name)
        self.pushButton_run_query.clicked.connect(self.run_query)
        self.pushButton_export.setEnabled(False)
        self.pushButton_export.clicked.connect(self.export)
        self.pushButton_export_close.clicked.connect(self.close_page)


    def run_query(self):
        #df_empty = pd.DataFrame()
        #model = pandasModel(df_empty)
        #self.tableView_result.setModel(model)
        query = self.textEdit_query.toPlainText()
        try:
            mydb = mysql.connector.connect(
                      host=self.hostname,
                      user=self.username,
                      password=self.password,
                      database=self.db_name
                    )

            mycursor = mydb.cursor()
            mycursor.execute("""{x}""".format(x=query))

            myresult = mycursor.fetchall()
            self.df_result = pd.DataFrame.from_records(myresult, columns=list(mycursor.column_names))

            df_empty = pd.DataFrame(columns=list(mycursor.column_names))
            model = pandasModel(df_empty)
            self.tableView_result.setModel(model)

            model = pandasModel(self.df_result)
            self.tableView_result.setModel(model)
            self.pushButton_export.setEnabled(True)
        except mysql.connector.Error as e:
            s = str(e)
            self.label_status.setText(s)

    def export(self):
        filename_export = QFileDialog.getSaveFileName(self, "Save file", "", ".xlsx")
        print(filename_export)
        my_path = filename_export[0] + ".xlsx"
        print(my_path)
        self.df_result.to_excel(my_path)

    def close_page(self):
        self.close()


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
