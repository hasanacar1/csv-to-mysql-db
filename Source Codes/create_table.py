from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
import mysql.connector
import csv

#, mydb, df_csv
class create_table_page(QDialog):
    def __init__(self, db_name, df_csv, hostname, username, password, csv_path):
        super().__init__()
        loadUi("create_table_2.ui", self)
        self.setWindowTitle("Create Table")
        self.csv_path = csv_path
        self.df_csv = df_csv
        self.db_name = db_name
        self.hostname = hostname
        self.username = username
        self.password = password
        self.listWidget_csv_columns.addItems(self.df_csv.columns.to_list())
        self.comboBox_data_type.addItems(['VARCHAR(255)', 'DATE', 'DATETIME', 'CHAR(255)', 'LONGTEXT', 'INTEGER(255)'])
        self.comboBox_data_type.setEnabled(False)
        self.progressBar.setValue(0)

        self.table_item_list = []
        self.pushButton_OK.clicked.connect(self.leave_from_page)
        self.pushButton_forward.clicked.connect(self.forward_item)
        self.pushButton_undo.clicked.connect(self.undo_item)
        self.pushButton_create_table.clicked.connect(self.create_table)

    def forward_item(self):
        try :
            selected_item = self.listWidget_csv_columns.takeItem(self.listWidget_csv_columns.currentRow())
            selected_item = selected_item.text() + " {x}".format(x=self.comboBox_data_type.currentText())
            self.table_item_list.append(selected_item)
            self.listWidget_table_columns.addItem(selected_item)
        except:
            print("no selected")

    def undo_item(self):
        try :
            selected_item = self.listWidget_table_columns.takeItem(self.listWidget_table_columns.currentRow())
            selected_item = selected_item.text()
            self.table_item_list.remove(selected_item)
            selected_item = selected_item.replace(" " + self.comboBox_data_type.currentText(), "")
            self.listWidget_csv_columns.addItem(selected_item)
        except :
            print("no selected")

    def create_table(self):
        data_specifier_str = "("
        create_table_str = "("
        table_column_list = []
        for item in self.table_item_list:
            create_table_str = create_table_str + item + ","
            data_specifier_str = data_specifier_str + "%s,"
            item_temp = item.replace(" VARCHAR(255)", "")
            table_column_list.append(item_temp)

        print(table_column_list)
        create_table_str = create_table_str[:-1] + ")"
        data_specifier_str = data_specifier_str[:-1] + ")"


        print(data_specifier_str)
        print(create_table_str)
        print(self.report_name_lineEdit.text())

        try :
            mydb = mysql.connector.connect(
                      host=self.hostname,
                      user=self.username,
                      password=self.password,
                      database=self.db_name
                    )

            mycursor = mydb.cursor()

            table_name = self.report_name_lineEdit.text()
            mycursor.execute("CREATE TABLE {y} {x}".format(x=create_table_str, y=table_name))
            #self.mydb.commit()

            insert_into_str = create_table_str.replace("VARCHAR(255)", "")

            print(insert_into_str)
            sql = "INSERT INTO {x} {y} VALUES {z}".format(x=table_name, y=insert_into_str, z=data_specifier_str)

            with open(self.csv_path) as f:
                val = []
                for count, line in enumerate(csv.reader(f, delimiter=';')):
                    if count == 0:
                        index_list = []
                        for column in table_column_list:
                            for i in range(0, len(table_column_list)):
                                if column == line[i]:
                                    index_list.append(i)
                        print(index_list)
                    else:
                        data = []
                        for index in index_list:
                            data.append(line[index])

                        val.append(tuple(data))

                    if count % 1000 == 0 and count != 0:
                        mycursor.executemany(sql, val)
                        mydb.commit()
                        val = []

            self.progressBar.setValue(100)
            self.label_status.setText("Created and Loaded")
        except mysql.connector.Error as e:
            self.label_status.setText(str(e))
        except :
            self.label_status.setText("Not Created and Loaded")


    def leave_from_page(self):
        self.close()

