# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '7Inv_contact.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):


    def press_ok(self, Dialog):
        Dialog.close()



    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 352)


        self.okay_btn = QtWidgets.QPushButton(Dialog, clicked=lambda: self.press_ok(Dialog))
        self.okay_btn.setGeometry(QtCore.QRect(30, 280, 341, 41))


        font = QtGui.QFont()
        font.setFamily("SF Pro Display")
        font.setPointSize(9)
        self.okay_btn.setFont(font)
        self.okay_btn.setObjectName("okay_btn")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(150, 30, 100, 100))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("[SUB] Information Management/Transaction-Management-System-main/Transaction-Management-System/POP_UP/1-Categories/delete_warning.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 120, 391, 71))
        font = QtGui.QFont()
        font.setFamily("SF Pro Display")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 180, 391, 71))
        font = QtGui.QFont()
        font.setFamily("SF Pro Display")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.okay_btn.setText(_translate("Dialog", "Okay"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Invalid contact number</p></body></html>"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Please make sure to enter numbers and <br/>not any other character.</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
