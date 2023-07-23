import sqlite3
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QDialog, QLineEdit, QPushButton

import os




class DBConnect(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Customer")

        self.phone_number = QLineEdit()
        self.name = QLineEdit()

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_customer)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.phone_number)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

        self.db_conn = sqlite3.connect("BDPS_dbconnect/BDPS.db")

    def add_customer(self):
        phone_number = self.phone_number.text()
        name = self.name.text()

        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO customer(CUST_NAME, CUST_CN) VALUES (?, ?)", (phone_number, name))
        self.db_conn.commit()

        self.phone_number.setText("")
        self.name.setText("")

    def __del__(self):
        self.db_conn.close()

app = QApplication([])
dialog = DBConnect()
dialog.show()
app.exec()
