import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from Functions import BtnFunctions

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    style_file = QFile("style.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())

    Functions = BtnFunctions()
    Functions.show()

    Functions.get_recent_transactions()

    sys.exit(app.exec())


 


