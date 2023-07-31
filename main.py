import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from Functions import BtnFunctions

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ## loading style file
    # with open("style.qss", "r") as style_file:
    #     style_str = style_file.read()
    # app.setStyleSheet(style_str)
    
    ## loading style file, Example 2
    style_file = QFile("style.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())

    Functions = BtnFunctions()
    Functions.show()

    sys.exit(app.exec())


    # fucking leg8t 


