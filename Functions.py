import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QFileDialog, QLineEdit
#from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream, QDate
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
        self.ui.no_transaction_found.hide()            

        
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)
        
        #========================== UPDATE =====================================#
        self.ui.update_transaction.pressed.connect(self.update_transaction_pressed)
        
        #========================== RESET OF TABLES =====================================#
        self.ui.pushButton_4.clicked.connect(self.reset_dailytxn_table)
        self.ui.pushButton_5.clicked.connect(self.reset_txn_table)
        #========================== DASHBOARD =====================================#
        self.ui.transaction_record_tbl.model().rowsRemoved.connect(self.count_transaction_record)
        self.ui.transaction_record_tbl.model().rowsInserted.connect(self.count_transaction_record)
        #self.ui.pushButton_3.clicked.connect(self.delete_selected_row)
        self.count_transaction_record()
        
        #========================== SEARCH FIELDS =====================================#
        self.ui.edit_search_pricelist.textChanged.connect(self.pricelist_table)
        self.ui.edit_search_category.textChanged.connect(self.category_table)
        self.ui.edit_search_daily_tnx.textChanged.connect(self.filter_dailytxn_table)
        self.ui.edit_search_dwt.textChanged.connect(self.datewise_txn_table)
        self.ui.edit_search_dwp.textChanged.connect(self.datewise_payment_table)
        self.ui.edit_search_new_transaction.textChanged.connect(self.transaction_table)

        #========================== FILTERING =====================================#
        self.ui.filter_daily_tnx.currentIndexChanged.connect(self.filter_dailytxn_table)
        #self.ui.filter_dwt.currentIndexChanged.connect(self.filter_datewise_txn_table)
        #self.ui.filter_dwp.currentIndexChanged.connect(self.filter_date_wise_payment_table) 
        
        self.ui.dateEdit_daily_tnx.dateChanged.connect(self.filter_bydate_dailytxn_table)
        #========================== EXCEL EXPORT BUTTONS =====================================#
        self.ui.printreport_dwp_btn.clicked.connect(self.datewise_payment_toExcel)
        self.ui.printreport_daily_tnx_btn.clicked.connect(self.daily_transaction_toExcel)
        self.ui.printreport_dwt_btn.clicked.connect(self.datewise_transaction_toExcel)

        #================================== TABLES ===============================#
        self.ui.category_table.horizontalHeader().setVisible(True)
        self.ui.pricelist_table.horizontalHeader().setVisible(True)

        self.ui.category_table.clicked.connect(self.on_service_row_clicked)
        self.ui.pricelist_table.clicked.connect(self.on_pricelist_row_clicked)

        #========================== DATABASE PATH =====================================#
        dbFolder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'BDPS_db/BDPS.db'))
        DBQueries.main(dbFolder)

        #======================== FETCH and MOD SERVICES =================================#
        DBQueries.displayServices(self, DBQueries.getAllServices(dbFolder))

        self.ui.add_category_btn.clicked.connect(lambda: DBQueries.addService(self, dbFolder))
        self.ui.edit_category_btn.clicked.connect(lambda: DBQueries.editService(self, dbFolder))
        self.ui.delete_category_btn.clicked.connect(lambda: DBQueries.deleteService(self, dbFolder))

        self.ui.category_table.itemSelectionChanged.connect(lambda: DBQueries.on_service_selection_changed(self))
        
        #======================== FETCH and MOD PRICELIST =================================#
        service_names = DBQueries.getServiceNames(dbFolder)
        self.ui.cat_name_pricelist.addItems(service_names)

        DBQueries.displayPrices(self, DBQueries.getAllPrices(dbFolder))

        self.ui.add_item_pricelist_btn.clicked.connect(lambda: DBQueries.addPrice(self, dbFolder))
        self.ui.update_pricelist_btn.clicked.connect(lambda: DBQueries.editPrice(self, dbFolder))
        self.ui.delete_pricelist_btn.clicked.connect(lambda: DBQueries.deletePrice(self, dbFolder))

        self.ui.pricelist_table.itemSelectionChanged.connect(lambda: DBQueries.on_price_selection_changed(self))

        #======================== FETCH and MOD JOBS =================================#
        #DBQueries.displayJobs(self, DBQueries.getAllJobs(dbFolder))
        self.ui.category_name_nt.addItems(service_names)
        
        sizes = DBQueries.getProductSizes(self, dbFolder)

        self.ui.category_name_nt.currentIndexChanged.connect(lambda: DBQueries.getProductSizes(self, dbFolder))

        self.ui.add_order_nt.clicked.connect(lambda: DBQueries.addJob(self, dbFolder))
        self.ui.delete_job_detail_btn.clicked.connect(lambda: DBQueries.deleteJob(self, dbFolder))
        self.ui.reset_job_detail_btn.clicked.connect(lambda: DBQueries.transfer_data_from_job_temp_to_jobs(self, dbFolder))

        self.ui.order_detail_table.itemSelectionChanged.connect(lambda: DBQueries.on_job_selection_changed(self))
        
        #======================== SEARCH FIELDS FUNCTIONS =================================#
        
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
            
    #Transaction records search field   
    def transaction_table(self):
        search_transaction = self.ui.edit_search_new_transaction.text().strip()

        # Check if the search field is empty
        if not search_transaction:
        # If the search field is empty, reset the QTableWidget to show all items
            for row in range(self.ui.transaction_record_tbl.rowCount()):
                self.ui.transaction_record_tbl.setRowHidden(row, False)
                self.ui.transaction_record_tbl.show()
                self.ui.no_transaction_found.hide()            
        
        row_matches = False
            
        for row in range(self.ui.transaction_record_tbl.rowCount()):
            for col in range(self.ui.transaction_record_tbl.columnCount()):
                item = self.ui.transaction_record_tbl.item(row, col)
                
                if item is not None and search_transaction.lower() in item.text().lower():
                    self.ui.transaction_record_tbl.setRowHidden(row, False)
                    row_matches = True
                    self.ui.transaction_record_tbl.show()
                    self.ui.no_transaction_found.hide()            
                    break
                else:
                    self.ui.transaction_record_tbl.setRowHidden(row, True)
        
        if not row_matches:
            self.ui.transaction_record_tbl.hide()
            self.ui.no_transaction_found.show()                       
            
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

        #======================== FILTER FUNCTIONS =================================#
              
    #Daily Transaction Filter 
    def filter_dailytxn_table(self):
        selected_item = self.ui.filter_daily_tnx.currentText()
        search_dailytxn = self.ui.edit_search_daily_tnx.text().strip().lower()
    
        no_row_matches = True
        
        for row in range(self.ui.daily_tnx_table.rowCount()):
            status_item = self.ui.daily_tnx_table.item(row, 3)
            for col in range(self.ui.daily_tnx_table.columnCount()):
                item = self.ui.daily_tnx_table.item(row, col)
            
                if status_item is not None and item is not None:
                    status = status_item.text().strip()
                    if (selected_item == "All Transactions") and (search_dailytxn in item.text().lower()):
                        self.ui.daily_tnx_table.setRowHidden(row, False)
                        self.ui.daily_tnx_table.show()
                        self.ui.no_dailytxn_found.hide()
                        self.ui.edit_search_daily_tnx.setEnabled(True)
                        no_row_matches = False
                        break
                    elif (selected_item == "Pending Transactions" and status == "Pending") and (search_dailytxn in item.text().lower()):
                        self.ui.daily_tnx_table.setRowHidden(row, False)
                        self.ui.daily_tnx_table.show()
                        self.ui.no_dailytxn_found.hide()
                        self.ui.edit_search_daily_tnx.setEnabled(True)
                        no_row_matches = False
                        break
                    elif (selected_item == "Failed Transactions" and status == "Failed") and (search_dailytxn in item.text().lower()):
                        self.ui.daily_tnx_table.setRowHidden(row, False)
                        self.ui.daily_tnx_table.show()
                        self.ui.no_dailytxn_found.hide()
                        self.ui.edit_search_daily_tnx.setEnabled(True)
                        no_row_matches = False
                        break
                    elif (selected_item == "Successful Transactions" and status == "Successful") and (search_dailytxn in item.text().lower()):
                        self.ui.daily_tnx_table.setRowHidden(row, False)
                        self.ui.daily_tnx_table.show()
                        self.ui.no_dailytxn_found.hide()
                        self.ui.edit_search_daily_tnx.setEnabled(True)
                        no_row_matches = False
                        break 
                    else:
                        self.ui.daily_tnx_table.setRowHidden(row, True)
        
        if no_row_matches == True:
            self.ui.daily_tnx_table.hide()
            self.ui.no_dailytxn_found.setText(f"There is no {selected_item} found.")
            self.ui.no_dailytxn_found.show()
        else:
            self.ui.daily_tnx_table.show()
            self.ui.no_dailytxn_found.hide()
            
    #Date-wise transaction filter button
    def filter_date_wise_transaction_clicked(self):
        print("date-wise transactions filter")  
                    
    #Date-wise payment filter button
    def filter_date_wise_payment_clicked(self):
        print("date-wise payment filter")
        
        #======================== FILTER BY DATE AND STATUS =================================#

    def filter_bydate_dailytxn_table(self):
        selected_date = self.ui.dateEdit_daily_tnx.date()
        new_date = selected_date.toString("yyyy-MM-dd") 
        selected_item = self.ui.filter_daily_tnx.currentText()
        search_dailytxn = self.ui.edit_search_daily_tnx.text().strip().lower()
        
        for row in range(self.ui.daily_tnx_table.rowCount()):
            date_item = self.ui.daily_tnx_table.item(row, 1)
            status_item = self.ui.daily_tnx_table.item(row, 3)
            status = status_item.text().strip()
            for col in range(self.ui.daily_tnx_table.columnCount()):
                item = self.ui.daily_tnx_table.item(row, col)  
                       
                if (date_item is not None and date_item.text() == new_date) and (selected_item == "All Transactions"):
                    self.ui.daily_tnx_table.setRowHidden(row, False)
                    self.ui.edit_search_daily_tnx.setEnabled(False)
                    
                elif(date_item is not None and date_item.text() == new_date) and (selected_item == "Pending Transactions" and status == "Pending"):
                    self.ui.daily_tnx_table.setRowHidden(row, False)
                    self.ui.edit_search_daily_tnx.setEnabled(False)
                    
                elif(date_item is not None and date_item.text() == new_date) and (selected_item == "Successful Transactions" and status == "Successful"):
                    self.ui.daily_tnx_table.setRowHidden(row, False)
                    self.ui.edit_search_daily_tnx.setEnabled(False)
                    
                elif(date_item is not None and date_item.text() == new_date) and (selected_item == "Failed Transactions" and status == "Failed"):
                    self.ui.daily_tnx_table.setRowHidden(row, False)
                    self.ui.edit_search_daily_tnx.setEnabled(False)

                else:
                    self.ui.daily_tnx_table.setRowHidden(row, True)
                    
        #======================== EXPORT FUNCTIONS =================================#
        
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
            
        #======================== RESET FUNCTIONS =================================#
        
    def reset_dailytxn_table(self):
        self.ui.edit_search_daily_tnx.setText("")  # Clear the search text
        self.ui.filter_daily_tnx.setCurrentIndex(0)  # Set the filter to the first item (or the default item)
        self.ui.dateEdit_daily_tnx.setDate(QDate.currentDate())  # Set the date to the current date
        
        for row in range(self.ui.daily_tnx_table.rowCount()):
            self.ui.daily_tnx_table.setRowHidden(row, False)        
            self.ui.daily_tnx_table.show()
            self.ui.no_dailytxn_found.hide()
            
    def reset_txn_table(self):
        #self.ui.edit_search_daily_tnx.setText("")  # Clear the search text
        #self.ui.filter_daily_tnx.setCurrentIndex(0)  # Set the filter to the first item (or the default item)
        #self.ui.dateEdit_daily_tnx.setDate(QDate.currentDate())  # Set the date to the current date
        
        for row in range(self.ui.transaction_record_tbl.rowCount()):
            self.ui.transaction_record_tbl.setRowHidden(row, False)        
            self.ui.transaction_record_tbl.show()
            self.ui.no_transaction_found.hide()            
                  
        #======================== DASHBOARD FUNCTIONS =================================#

    def count_transaction_record(self):
        total_transaction = self.ui.transaction_record_tbl.rowCount()
        self.ui.total_transactions.setText(f"{total_transaction}")            
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
    def on_service_row_clicked(self, index):
        selected_rows = self.ui.category_table.selectionModel().selectedRows()
        row = index.row()
        serv_id = self.ui.category_table.item(row, 0).text()
        serv_name = self.ui.category_table.item(row, 1).text()
        serv_desc = self.ui.category_table.item(row, 2).text()
        serv_sts = self.ui.category_table.item(row, 3).text()

        self.ui.id_category.setReadOnly(True)
        self.ui.id_category.setText(serv_id)
        self.ui.product_name_category.setPlaceholderText(serv_name)
        self.ui.category_description.setPlaceholderText(serv_desc)
        self.ui.status_category.setCurrentIndex(self.ui.status_category.findText(serv_sts))

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
    