from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox
#from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
#from PyQt5 import QtWidgets, QtGui, QtCore
from BDPS_ui import Ui_MainWindow
from BDPS_db.BDPS_queries import DBQueries


class BtnFunctions(QMainWindow):
    def __init__(self):
        super(BtnFunctions, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)
    
        self.ui.search_pricelist_btn.clicked.connect(self.pricelist_clicked)
        self.ui.edit_search_pricelist.textChanged.connect(self.pricelist_table_default)
        
        self.ui.search_category_btn.clicked.connect(self.category_clicked)
        self.ui.edit_search_category.textChanged.connect(self.category_table_default)

        self.ui.search_daily_tnx_btn.clicked.connect(self.daily_tnx_clicked)
        self.ui.filter_daily_tnx_btn.clicked.connect(self.filter_daily_tnx_clicked)
        
        self.ui.search_dwt_btn.clicked.connect(self.date_wise_transactions_clicked)
        self.ui.filter_dwt_btn.clicked.connect(self.filter_date_wise_transaction_clicked)
        
        self.ui.search_dwt_btn_4.clicked.connect(self.date_wise_payment_clicked)
        self.ui.filter_dwp_btn.clicked.connect(self.filter_date_wise_payment_clicked)
    
    #Set the Price list table to default    
    def pricelist_table_default(self):
        search_price = self.ui.edit_search_pricelist.toPlainText()
        
        # Check if the search field is empty
        if not search_price:
        # If the search field is empty, reset the QTableWidget to show all items
            for row in range(self.ui.pricelist_table.rowCount()):
                self.ui.pricelist_table.setRowHidden(row, False)
            return
        
        """
        for row in range(self.ui.pricelist_table.rowCount()):
            row_matches = False
            for col in range(self.ui.pricelist_table.columnCount()):
                item = self.ui.pricelist_table.item(row, col)
                if item is not None and search_price.lower() in item.text().lower():
                    row_matches = True
                    break
            self.ui.pricelist_table.setRowHidden(row, not row_matches)
        """
        
    # Price list search button   
    def pricelist_clicked(self):
        search_price = self.ui.edit_search_pricelist.toPlainText()
     #  self.ui.pricelist_table.clearContents()
        if not search_price:
            QMessageBox.warning(self, "Empty Text", "The text is empty. Please enter some text.")
            
        for row in range(self.ui.pricelist_table.rowCount()):
            row_matches = False
            for col in range(self.ui.pricelist_table.columnCount()):
                item = self.ui.pricelist_table.item(row, col)

                if item is not None and search_price.lower() in item.text().lower():
                    row_matches = True
                    break
            self.ui.pricelist_table.setRowHidden(row, not row_matches)

    #Set the Price list table to default    
    def category_table_default(self):
        search_category = self.ui.edit_search_category.toPlainText()
        
        # Check if the search field is empty
        if not search_category:
        # If the search field is empty, reset the QTableWidget to show all items
            for row in range(self.ui.category_table.rowCount()):
                self.ui.category_table.setRowHidden(row, False)
            return

    # Category search button 
    def category_clicked(self):
        search_category = self.ui.edit_search_category.toPlainText()
     #  self.ui.pricelist_table.clearContents()
        if not search_category:
            QMessageBox.warning(self, "Empty Text", "The text is empty. Please enter some text.")
            
        for row in range(self.ui.category_table.rowCount()):
            row_matches = False
            for col in range(self.ui.category_table.columnCount()):
                item = self.ui.category_table.item(row, col)

                if item is not None and search_category.lower() in item.text().lower():
                    row_matches = True
                    break
            self.ui.category_table.setRowHidden(row, not row_matches)
    
                
    #Daily Transaction search button
    def daily_tnx_clicked(self):
        print("daily")
        
    #Daily Transaction filter button
    def filter_daily_tnx_clicked(self):
        print("filter daily")
    
    #Date-wise transactions search button
    def date_wise_transactions_clicked(self):
        print("date-wise transactions")
    
    #Date-wise transaction filter button
    def filter_date_wise_transaction_clicked(self):
        print("date-wise transactions filter")
    
    #Date-wise payments search button
    def date_wise_payment_clicked(self):
        print("date-wise payments")
    
    #Date-wise transaction filter button
    def filter_date_wise_payment_clicked(self):
        print("date-wise payment filter")
                
    #----------------------------------------------------------------------#
    
    ## Function for searching
    def on_search_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        search_text = self.ui.search_input.text().strip()
        if search_text:
            self.ui.label_9.setText(search_text)

    ## Function for changing page to user page
    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                    + self.ui.full_menu_widget.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [7, 8]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
            
    ## ----------------------- functions for changing menu page ---------------------
    def on_home_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_home_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_price_list_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_price_list_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_categories_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_categories_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_new_transaction_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_new_transaction_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_transaction_record_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_transaction_record_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_daily_transaction_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def on_daily_transaction_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def on_daily_transaction_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    def on_datewise_transaction_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(6)
    
    def on_datewise_payment_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(7)

    def on_daily_payment_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(7)

     ## ----------------------- ADD SHADOW --------------------- 