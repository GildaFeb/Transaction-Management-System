import mysql.connector
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QDialog, QLineEdit, QPushButton

class Dialog(QDialog):

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

    def add_customer(self):
        phone_number = self.phone_number.text()
        name = self.name.text()

        db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "password",
            database = "BDPS_db"
        )

        cursor = db.cursor()
        cursor.execute("INSERT INTO customer (CUST_NAME, CUST_CN) VALUES (%s, %s)", (phone_number, name))

        db.commit()

        cursor.close()
        db.close()

        self.phone_number.setText("")
        self.name.setText("")

app = QApplication([])
dialog = Dialog()
dialog.show()
app.exec()
