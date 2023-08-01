import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QFileDialog, QLineEdit
#from PyQt5.QtGui import QStandardItemModel, QStandardItem
#from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
#from PyQt5 import QtWidgets, QtGui, QtCore
from openpyxl import load_workbook, Workbook
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
        #========================== SEARCH FIELDS =====================================#
        self.ui.update_transaction.pressed.connect(self.update_transaction_pressed)

        #========================== SEARCH FIELDS =====================================#
        self.ui.edit_search_pricelist.textChanged.connect(self.pricelist_table)
        self.ui.edit_search_category.textChanged.connect(self.category_table)
        self.ui.edit_search_daily_tnx.textChanged.connect(self.daily_tnx_table)
        self.ui.edit_search_dwt.textChanged.connect(self.datewise_txn_table)
        self.ui.edit_search_dwp.textChanged.connect(self.datewise_payment_table)

        #========================== FILTER BUTTONS =====================================#
        self.ui.filter_daily_tnx_btn.clicked.connect(self.filter_daily_tnx_clicked) 
        self.ui.filter_dwt_btn.clicked.connect(self.filter_date_wise_transaction_clicked)      
        self.ui.filter_dwp_btn.clicked.connect(self.filter_date_wise_payment_clicked)
        
        #========================== EXCEL EXPORT BUTTONS =====================================#
        self.ui.printreport_dwp_btn.clicked.connect(self.datewise_payment_toExcel)
        self.ui.printreport_daily_tnx_btn.clicked.connect(self.daily_transaction_toExcel)
        self.ui.printreport_dwt_btn.clicked.connect(self.datewise_transaction_toExcel)

        #================================== TABLES ===============================#
        self.ui.category_table.horizontalHeader().setVisible(True)
        self.ui.pricelist_table.horizontalHeader().setVisible(True)

        self.ui.category_table.clicked.connect(self.on_category_row_clicked)
        self.ui.pricelist_table.clicked.connect(self.on_pricelist_row_clicked)

        #========================== DATABASE PATH =====================================#
        dbFolder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'BDPS_db/BDPS.db'))
        DBQueries.main(dbFolder)

        #======================== FETCH and MOD CATEGORIES =================================#
        DBQueries.displayCategories(self, DBQueries.getAllCategories(dbFolder))

        self.ui.add_category_btn.clicked.connect(lambda: DBQueries.addCategory(self, dbFolder))
        self.ui.edit_category_btn.clicked.connect(lambda: DBQueries.editCategory(self, dbFolder))
        self.ui.delete_category_btn.clicked.connect(lambda: DBQueries.deleteCategory(self, dbFolder))

        self.ui.category_table.itemSelectionChanged.connect(lambda: DBQueries.on_category_selection_changed(self))
        
        #======================== FETCH and MOD PRICELIST =================================#
        category_names = DBQueries.getCategoryNames(dbFolder)
        self.ui.cat_name_pricelist.addItems(category_names)

        DBQueries.displayPrices(self, DBQueries.getAllPrices(dbFolder))

        self.ui.add_item_pricelist_btn.clicked.connect(lambda: DBQueries.addPrice(self, dbFolder))
        self.ui.update_pricelist_btn.clicked.connect(lambda: DBQueries.editPrice(self, dbFolder))
        self.ui.delete_pricelist_btn.clicked.connect(lambda: DBQueries.deletePrice(self, dbFolder))

        self.ui.pricelist_table.itemSelectionChanged.connect(lambda: DBQueries.on_price_selection_changed(self))

        #======================== FETCH and MOD ORDERS =================================#
        DBQueries.displayOrders(self, DBQueries.getAllOrders(dbFolder))
        self.ui.category_name_nt.addItems(category_names)
        
        selected_category = self.ui.category_name_nt.currentText()
        sizes = DBQueries.getProductSizes(self, dbFolder)
        self.ui.category_size.addItems(sizes)
        self.ui.category_name_nt.currentIndexChanged.connect(lambda: DBQueries.getProductSizes(self, dbFolder))
        
    #Price list search field    
    def pricelist_table(self):
        search_pricelist = self.ui.edit_search_pricelist.text().strip()

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
        search_category = self.ui.edit_search_category.text().strip()

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

        #======================== END OF SEARCH FIELDS FUNCTIONS =================================#
                
    #Daily Transaction filter button
    def filter_daily_tnx_clicked(self):
        print("filter daily")
              
    #Date-wise transaction filter button
    def filter_date_wise_transaction_clicked(self):
        print("date-wise transactions filter")  
                    
    #Date-wise payment filter button
    def filter_date_wise_payment_clicked(self):
        print("date-wise payment filter")
        
        #======================== END OF FILTER FUNCTIONS =================================#
    #Daily Transaction to Excel
    def daily_transaction_toExcel(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx);;All Files (*)")

        if path:
            sample = None
            try:
                sample = load_workbook(path)
            except FileNotFoundError:
                sample = Workbook()
                    
            data = sample.active
            
            headers = [self.ui.daily_tnx_table.horizontalHeaderItem(i).text() for i in range(self.ui.daily_tnx_table.columnCount())]
                
            for column_index, header in enumerate(headers, start = 1):
                data.cell(row=1, column = column_index, value = header)
                    
            for row in range(self.ui.daily_tnx_table.rowCount()):
                for col in range(self.ui.daily_tnx_table.columnCount()):
                    items = self.ui.daily_tnx_table.item(row, col)
                    if items is not None:
                        data.cell(row=row + 2, column = col + 1, value = items.text())
                
            sample.save(path)
            
    #Date-wise Transaction to Excel        
    def datewise_transaction_toExcel(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx);;All Files (*)")

        if path:
            sample = None
            try:
                sample = load_workbook(path)
            except FileNotFoundError:
                sample = Workbook()
                    
            data = sample.active
            
            headers = [self.ui.datewise_transaction_table.horizontalHeaderItem(i).text() for i in range(self.ui.datewise_transaction_table.columnCount())]
                
            for column_index, header in enumerate(headers, start = 1):
                data.cell(row=1, column = column_index, value = header)
                    
            for row in range(self.ui.datewise_transaction_table.rowCount()):
                for col in range(self.ui.datewise_transaction_table.columnCount()):
                    items = self.ui.datewise_transaction_table.item(row, col)
                    if items is not None:
                        data.cell(row=row + 2, column = col + 1, value = items.text())
                
            sample.save(path)                      
    
    #Date-wise Payment to Excel
    def datewise_payment_toExcel(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx);;All Files (*)")

        if path:
            sample = None
            try:
                sample = load_workbook(path)
            except FileNotFoundError:
                sample = Workbook()
                    
            data = sample.active
            
            headers = [self.ui.datewise_payment_table.horizontalHeaderItem(i).text() for i in range(self.ui.datewise_payment_table.columnCount())]
                
            for column_index, header in enumerate(headers, start = 1):
                data.cell(row=1, column = column_index, value = header)
                    
            for row in range(self.ui.datewise_payment_table.rowCount()):
                for col in range(self.ui.datewise_payment_table.columnCount()):
                    items = self.ui.datewise_payment_table.item(row, col)
                    if items is not None:
                        data.cell(row=row + 2, column = col + 1, value = items.text())
                
            sample.save(path)  
            
        #======================== END OF EXPORT FUNCTIONS =================================#

                
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

    def update_transaction_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(8)

     ## ----------------------- ADD SHADOW --------------------- 


    #========================== SETTING PLACEHOLDERS =========================#    
    def on_category_row_clicked(self, index):
        selected_rows = self.ui.category_table.selectionModel().selectedRows()
        row = index.row()
        cat_id = self.ui.category_table.item(row, 0).text()
        cat_name = self.ui.category_table.item(row, 1).text()
        cat_desc = self.ui.category_table.item(row, 2).text()
        cat_sts = self.ui.category_table.item(row, 3).text()

        self.ui.id_category.setReadOnly(True)
        self.ui.id_category.setText(cat_id)
        self.ui.product_name_category.setPlaceholderText(cat_name)
        self.ui.category_description.setPlaceholderText(cat_desc)
        self.ui.status_category.setCurrentIndex(self.ui.status_category.findText(cat_sts))

        if len(selected_rows) != 1:
            self.ui.id_category.setReadOnly(True)
            self.ui.id_category.setText('')
            self.ui.product_name_category.setPlaceholderText('')
            self.ui.category_description.setPlaceholderText('')
            self.ui.status_category.setCurrentIndex(-1)
    
    def on_pricelist_row_clicked(self, index):
        selected_rows = self.ui.pricelist_table.selectionModel().selectedRows()
        row = index.row()
        prod_id = self.ui.pricelist_table.item(row, 0).text()
        cat_name = self.ui.pricelist_table.item(row, 1).text()
        prod_sz = self.ui.pricelist_table.item(row, 2).text()
        prod_price = self.ui.pricelist_table.item(row, 3).text()

        self.ui.id_pricelist.setReadOnly(True)
        self.ui.id_pricelist.setText(prod_id)
        self.ui.cat_name_pricelist.setCurrentIndex(self.ui.cat_name_pricelist.findText(cat_name))
        self.ui.size_pricelist.setPlaceholderText(prod_sz)
        self.ui.price_pricelist.setPlaceholderText(prod_price)

        if len(selected_rows) != 1:
            self.ui.id_pricelist.setText('')
            self.ui.cat_name_pricelist.setCurrentIndex(-1)
            self.ui.size_pricelist.setPlaceholderText('')
            self.ui.price_pricelist.setPlaceholderText('')
            