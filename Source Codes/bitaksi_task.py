from server_connection import server_connection_page
from PyQt5.QtWidgets import *

if __name__ == "__main__":
    app = QApplication([])
    window = server_connection_page()
    #window.showMaximized()
    window.show()
    app.exec_()
