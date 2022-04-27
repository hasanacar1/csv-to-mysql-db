from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import mysql.connector
from import_csv import import_csv_page
from mysql.connector import errors

class server_connection_page(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("server_connection.ui", self)
        # set the title
        self.setWindowTitle("MySQL Server Connection")
        self.pushButton_connect_server.clicked.connect(self.server_conn_func)

    def server_conn_func(self):
        hostname = self.lineEdit_hostname.text()
        port = self.lineEdit_port.text()
        password = self.lineEdit_password.text()
        username = self.lineEdit_username.text()
        db_name = self.lineEdit_db_name.text()

        try :
            mydb = mysql.connector.connect(
                  host=hostname,
                  user=username,
                  password=password
                )
            mycursor = mydb.cursor()
            mycursor.execute("CREATE DATABASE {x}".format(x=db_name))
            self.label_status.setText("Connected and created db")

            self.import_csv_obj = import_csv_page(mydb, hostname, username, password, db_name)
            self.import_csv_obj.show()
            self.import_csv_obj.exec_()
        except mysql.connector.Error as e:
            self.label_status.setText(str(e))
        except :
            print(mysql.connector.Error)
            #self.label_status.setText(str(mysql.connector.Error))

        '''
        except mysql.connector.Error as e:
            s = str(e)
            self.label_status.setText(s)
        '''
