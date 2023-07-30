import os
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
        
        self.ui.no_category_found.hide()
        self.ui.no_pricelist_found.hide()
        self.ui.no_dailytxn_found.hide()
        self.ui.no_datewiseT_found.hide()
        self.ui.no_datewiseP_found.hide()
        
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)
    
        self.ui.edit_search_pricelist.textChanged.connect(self.pricelist_table)
        
        self.ui.edit_search_category.textChanged.connect(self.category_table)

        self.ui.edit_search_daily_tnx.textChanged.connect(self.daily_tnx_table)
        self.ui.filter_daily_tnx_btn.clicked.connect(self.filter_daily_tnx_clicked)
        
        self.ui.edit_search_dwt.textChanged.connect(self.datewise_txn_table)
        self.ui.filter_dwt_btn.clicked.connect(self.filter_date_wise_transaction_clicked)
        
        self.ui.edit_search_dwp.textChanged.connect(self.datewise_payment_table)
        self.ui.filter_dwp_btn.clicked.connect(self.filter_date_wise_payment_clicked)

        #========================== DATABASE PATH =====================================#
        dbFolder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'BDPS_db/BDPS.db'))
        DBQueries.main(dbFolder)

        #======================== FETCH and MOD CATEGORIES =================================#
        DBQueries.displayCategories(self, DBQueries.getAllCategories(dbFolder))

        self.ui.add_category_btn.clicked.connect(lambda: DBQueries.addCategory(self, dbFolder))
        self.ui.edit_category_btn.clicked.connect(lambda: DBQueries.editCategory(self, dbFolder))
        self.ui.delete_category_btn.clicked.connect(lambda: DBQueries.deleteCategory(self, dbFolder))

        self.ui.category_table.itemSelectionChanged.connect(lambda: DBQueries.on_category_selection_changed(self))
        self.ui.category_table.selectionModel().selectionChanged.connect(lambda: DBQueries.on_selection_changed(self))

    #Price list search field    
    def pricelist_table(self):
        search_pricelist = self.ui.edit_search_pricelist.toPlainText()

        # Check if the search field is empty
        if not search_pricelist:
        # If the search field is empty, reset the QTableWidget to show all items
            for row in range(self.ui.pricelist_table.rowCount()):
                self.ui.pricelist_table.setRowHidden(row, False)
                self.ui.pricelist_table.show()
                self.ui.no_pricelist_found.hide()
        
        row_matches = False
            
        for row in range(self.ui.pricelist_table.rowCount()):
            for col in range(self.ui.pricelist_table.columnCount()):
                item = self.ui.pricelist_table.item(row, col)
                
                if item is not None and search_pricelist.lower() in item.text().lower():
                    self.ui.pricelist_table.setRowHidden(row, False)
                    row_matches = True
                    self.ui.pricelist_table.show()
                    self.ui.no_pricelist_found.hide()
                    break
                else:
                    self.ui.pricelist_table.setRowHidden(row, True)
        
        if not row_matches:
            self.ui.pricelist_table.hide()
            self.ui.no_pricelist_found.show()

    #Category search field   
    def category_table(self):
        search_category = self.ui.edit_search_category.toPlainText()

        # Check if the search field is empty
        if not search_category:
        # If the search field is empty, reset the QTableWidget to show all items
            for row in range(self.ui.category_table.rowCount()):
                self.ui.category_table.setRowHidden(row, False)
                self.ui.category_table.show()
                self.ui.no_category_found.hide()            
        
        row_matches = False
            
        for row in range(self.ui.category_table.rowCount()):
            for col in range(self.ui.category_table.columnCount()):
                item = self.ui.category_table.item(row, col)
                
                if item is not None and search_category.lower() in item.text().lower():
                    self.ui.category_table.setRowHidden(row, False)
                    row_matches = True
                    self.ui.category_table.show()
                    self.ui.no_category_found.hide()
                    break
                else:
                    self.ui.category_table.setRowHidden(row, True)
        
        if not row_matches:
            self.ui.category_table.hide()
            self.ui.no_category_found.show()
            
    #Daily Transaction search field
    def daily_tnx_table(self):
        search_dailytxn = self.ui.edit_search_daily_tnx.text().strip()

        # Check if the search field is empty
        if not search_dailytxn:
        # If the search field is empty, reset the QTableWidget to show all items
            for row in range(self.ui.daily_tnx_table.rowCount()):
                self.ui.daily_tnx_table.setRowHidden(row, False)
                self.ui.daily_tnx_table.show()
                self.ui.no_dailytxn_found.hide()
        
        row_matches = False
            
        for row in range(self.ui.daily_tnx_table.rowCount()):
            for col in range(self.ui.daily_tnx_table.columnCount()):
                item = self.ui.daily_tnx_table.item(row, col)
                
                if item is not None and search_dailytxn.lower() in item.text().lower():
                    self.ui.daily_tnx_table.setRowHidden(row, False)
                    row_matches = True
                    self.ui.daily_tnx_table.show()
                    self.ui.no_dailytxn_found.hide()
                    break
                else:
                    self.ui.daily_tnx_table.setRowHidden(row, True)
        
        if not row_matches:
            self.ui.daily_tnx_table.hide()
            self.ui.no_dailytxn_found.show()    
                
    #Daily Transaction filter button
    def filter_daily_tnx_clicked(self):
        print("filter daily")
    
    #Date-wise transactions search field
    def datewise_txn_table(self):
        search_datewise_txn = self.ui.edit_search_dwt.text().strip()

        # Check if the search field is empty
        if not search_datewise_txn:
        # If the search field is empty, reset the QTableWidget to show all items
            for row in range(self.ui.datewise_transaction_table.rowCount()):
                self.ui.datewise_transaction_table.setRowHidden(row, False)
                self.ui.datewise_transaction_table.show()
                self.ui.no_datewiseT_found.hide()
        
        row_matches = False
            
        for row in range(self.ui.datewise_transaction_table.rowCount()):
            for col in range(self.ui.datewise_transaction_table.columnCount()):
                item = self.ui.datewise_transaction_table.item(row, col)
                
                if item is not None and search_datewise_txn.lower() in item.text().lower():
                    self.ui.datewise_transaction_table.setRowHidden(row, False)
                    row_matches = True
                    self.ui.datewise_transaction_table.show()
                    self.ui.no_datewiseT_found.hide()
                    break
                else:
                    self.ui.datewise_transaction_table.setRowHidden(row, True)
        
        if not row_matches:
            self.ui.datewise_transaction_table.hide()
            self.ui.no_datewiseT_found.show()      
              
    #Date-wise transaction filter button
    def filter_date_wise_transaction_clicked(self):
        print("date-wise transactions filter")
    
    #Date-wise payments search field
    def datewise_payment_table(self):
        search_datewise_pay = self.ui.edit_search_dwp.text().strip()

        # Check if the search field is empty
        if not search_datewise_pay:
        # If the search field is empty, reset the QTableWidget to show all items
            for row in range(self.ui.datewise_payment_table.rowCount()):
                self.ui.datewise_payment_table.setRowHidden(row, False)
                self.ui.datewise_payment_table.show()
                self.ui.no_datewiseP_found.hide()
        
        row_matches = False
            
        for row in range(self.ui.datewise_payment_table.rowCount()):
            for col in range(self.ui.datewise_payment_table.columnCount()):
                item = self.ui.datewise_payment_table.item(row, col)
                
                if item is not None and search_datewise_pay.lower() in item.text().lower():
                    self.ui.datewise_payment_table.setRowHidden(row, False)
                    row_matches = True
                    self.ui.datewise_payment_table.show()
                    self.ui.no_datewiseP_found.hide()
                    break
                else:
                    self.ui.datewise_payment_table.setRowHidden(row, True)
        
        if not row_matches:
            self.ui.datewise_payment_table.hide()
            self.ui.no_datewiseP_found.show()  
                    
    #Date-wise payment filter button
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