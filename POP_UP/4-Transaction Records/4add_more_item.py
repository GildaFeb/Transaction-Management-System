# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '4add_more_item.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(660, 281)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 40, 200, 200))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("add.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.add_btn = QtWidgets.QPushButton(Dialog)
        self.add_btn.setGeometry(QtCore.QRect(280, 190, 131, 41))
        font = QtGui.QFont()
        font.setFamily("SF Pro Display")
        font.setPointSize(9)
        self.add_btn.setFont(font)
        self.add_btn.setDefault(False)
        self.add_btn.setFlat(False)
        self.add_btn.setObjectName("add_btn")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 190, 131, 41))
        font = QtGui.QFont()
        font.setFamily("SF Pro Display")
        font.setPointSize(9)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(280, 30, 391, 71))
        font = QtGui.QFont()
        font.setFamily("SF Pro Display")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(280, 90, 391, 71))
        font = QtGui.QFont()
        font.setFamily("SF Pro Display")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.add_btn.setText(_translate("Dialog", "Add"))
        self.pushButton_2.setText(_translate("Dialog", "Cancel"))
        self.label_2.setText(_translate("Dialog", "Add more order"))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p>Do you want to add more order?<br/>This can\'t be undone.</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
