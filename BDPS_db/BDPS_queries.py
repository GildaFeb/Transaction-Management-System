import os
import sys
import time
import sqlite3
from sqlite3 import Error
from datetime import datetime

#from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui

from openpyxl import load_workbook, Workbook

from POP_UP.add1 import Add_Categ
from POP_UP.edit_confirm_categ1 import Edit_Categ
from POP_UP.NoDetails8 import No_Details
from POP_UP.delete_confirm_categ1 import Del_Categ



class DBQueries():
    def __init__(self, arg):
        super(DBQueries, self).__init__()
        self.arg = arg
    
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        
        return conn
    
    def create_table(conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
    
    def main(dbFolder):
        conn = DBQueries.create_connection(dbFolder)

    #============================= SERVICE QUERIES =======================================#
    def getAllServices(dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        get_all_service = """ SELECT * FROM service; """

        try:
            c = conn.cursor()
            c.execute(get_all_service)

            return c
        except Error as e:
            print(e)

    def displayServices(self, rows):
        self.ui.category_table.setRowCount(0)

        for row in rows:
            rowPosition = self.ui.category_table.rowCount()

            if rowPosition > row[0]:
                continue

            itemCount = 0

            self.ui.category_table.setRowCount(rowPosition + 1)
            service_tablewidgetitem = QTableWidgetItem()
            self.ui.category_table.setVerticalHeaderItem(rowPosition, service_tablewidgetitem)

            for idx, item in enumerate(row):
                if idx == 0:
                    display_item = "S-" + str(item)
                else:
                    display_item = str(item)

                self.service_tablewidgetitem = QTableWidgetItem()
                self.ui.category_table.setItem(rowPosition, itemCount, self.service_tablewidgetitem)
                self.service_tablewidgetitem = self.ui.category_table.item(rowPosition, itemCount)
                self.service_tablewidgetitem.setText(display_item)

                itemCount = itemCount + 1
            rowPosition = rowPosition + 1

    
    def addService(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        service_name = self.ui.product_name_category.text()
        service_desc = self.ui.category_description.text()
        service_sts = self.ui.status_category.currentText()

        if not service_name or not service_desc:
# ================ PROMPT ================ #
            print("Missing fields.")
            return

        check_service_exists_sql = f"""
                                    SELECT SERV_ID FROM service
                                    WHERE SERV_NAME = '{service_name}'
                                    AND SERV_DESC = '{service_desc}'
                                    AND SERV_STS = '{service_sts}';
                                    """
        c = conn.cursor()
        c.execute(check_service_exists_sql)
        existing_service = c.fetchone()

        if existing_service:
# ================ PROMPT ================ #
            print("Service already exists.")
            return

        insert_service_data_sql = f""" 
                                        INSERT INTO service (SERV_NAME, SERV_DESC, SERV_STS) VALUES ('{service_name}','{service_desc}', '{service_sts}'); 
                                    """

        try:
            c = conn.cursor()
            c.execute(insert_service_data_sql)
            conn.commit()

            self.ui.product_name_category.setText("")
            self.ui.category_description.setText("")
            self.ui.status_category.itemText(0)

            service_names = DBQueries.getServiceNames(dbFolder)
            self.ui.cat_name_pricelist.clear()
            self.ui.cat_name_pricelist.addItems(service_names)

            DBQueries.displayServices(self, DBQueries.getAllServices(dbFolder))

        except Error as e:
            print(e)
    
    
    # === DRA ===
    def edit_no_service(self): # to open delete_confirm_categ
        self.window = QtWidgets.QMainWindow()
        self.ui = No_Details() # from other py file
        self.ui.setupUi(self.window)
        self.window.show()

    def editService(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        selected_row = self.ui.category_table.currentRow()
        if selected_row < 0:

            # ========================= PROMPT ========================= #

            # === DRA === #
            # === Edit Category Btn / No Service === #
            self.ui.edit_category_btn.clicked.connect(lambda: self.edit_no_service())
            #print("No service selected.")

            return
        

        service_id = int(self.ui.category_table.item(selected_row, 0).text().split('-')[-1])
        service_name = self.ui.product_name_category.text()
        service_desc = self.ui.category_description.text()
        service_sts = self.ui.status_category.currentText()

        get_service_data_sql = f"""
                                SELECT SERV_NAME, SERV_DESC, SERV_STS FROM service
                                WHERE SERV_ID = {service_id};
                                """
        c = conn.cursor()
        c.execute(get_service_data_sql)
        existing_data = c.fetchone()

        if not service_name:
            service_name = existing_data[0]
        if not service_desc:
            service_desc = existing_data[1]
        if not service_sts:
            service_sts = existing_data[2]

        check_service_exists_sql = f"""
                                    SELECT SERV_ID FROM service
                                    WHERE SERV_NAME = '{service_name}'
                                    AND SERV_DESC = '{service_desc}'
                                    AND SERV_STS = '{service_sts}'
                                    AND SERV_ID != {service_id};
                                    """
        c.execute(check_service_exists_sql)
        existing_service = c.fetchone()

        if existing_service:
# ================ PROMPT ================ #
            print("Service with updated values already exists in another row.")
            return

        if service_name == existing_data[0] and service_desc == existing_data[1] and service_sts == existing_data[2]:
# ================ PROMPT ================ #
            print("No changes made to the service details.")
            return

        update_service_data_sql = f""" 
                                        UPDATE service 
                                        SET SERV_NAME = '{service_name}', SERV_DESC = '{service_desc}', SERV_STS = '{service_sts}'
                                        WHERE SERV_ID = {service_id};
                                    """

        try:
            c = conn.cursor()
            c.execute(update_service_data_sql)
            conn.commit()

            self.ui.product_name_category.setText("")
            self.ui.category_description.setText("")
            self.ui.product_name_category.setPlaceholderText("")
            self.ui.category_description.setPlaceholderText("")
            self.ui.status_category.setCurrentIndex(0)


            service_names = DBQueries.getServiceNames(dbFolder)
            self.ui.cat_name_pricelist.clear()
            self.ui.cat_name_pricelist.addItems(service_names)

            DBQueries.displayServices(self, DBQueries.getAllServices(dbFolder))

        except Error as e:
            print(e)


    def deleteService(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        selected_rows = self.ui.category_table.selectionModel().selectedRows()
        if not selected_rows:
            
# =============== PROMPT ================= # (Same with the no service in edit)
            self.ui.edit_category_btn.clicked.connect(lambda: self.edit_no_service())

            print("No service selected.")
            return

        if len(selected_rows) == 1:
            service_id = int(self.ui.category_table.item(selected_rows[0].row(), 0).text().split('-')[-1])

            delete_service_sql = f"""
                                    DELETE FROM service
                                    WHERE SERV_ID = {service_id};
                                """

            try:
                c = conn.cursor()
                c.execute(delete_service_sql)
                conn.commit()

                service_names = DBQueries.getServiceNames(dbFolder)
                self.ui.cat_name_pricelist.clear()
                self.ui.cat_name_pricelist.addItems(service_names)

                DBQueries.displayServices(self, DBQueries.getAllServices(dbFolder))

            except Error as e:
                print(e)

        else:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Question)
            message_box.setText("You have selected multiple services. Are you sure you want to delete them?")
            message_box.setWindowTitle("Confirm Deletion")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            message_box.setDefaultButton(QMessageBox.No)

            response = message_box.exec()

            if response == QMessageBox.Yes:
                service_ids = [int(self.ui.category_table.item(row.row(), 0).text().split('-')[-1]) for row in selected_rows]

                delete_selected_service_sql = f"""
                                                DELETE FROM service
                                                WHERE SERV_ID IN ({', '.join(str(id) for id in service_ids)});
                                            """

                try:
                    c = conn.cursor()
                    c.execute(delete_selected_service_sql)
                    conn.commit()

                    service_names = DBQueries.getServiceNames(dbFolder)
                    self.ui.cat_name_pricelist.clear()
                    self.ui.cat_name_pricelist.addItems(service_names)

                    DBQueries.displayServices(self, DBQueries.getAllServices(dbFolder))

                except Error as e:
                    print(e)

    def on_service_selection_changed(self):
        selected_rows = self.ui.category_table.selectionModel().selectedRows()
        add_service_btn = self.ui.add_category_btn
        edit_service_btn = self.ui.edit_category_btn
        
        if len(selected_rows) > 0:
            add_service_btn.setVisible(False)
        else:
            add_service_btn.setVisible(True)
            
        if len(selected_rows) > 1:
            edit_service_btn.setVisible(False)
        else:
            edit_service_btn.setVisible(True)

    #======================= PRICE LIST QUERIES =========================#
    def getServiceNames(dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        get_service_names_sql = """SELECT SERV_NAME
                                    FROM service
                                    WHERE SERV_STS = 'Available';
                                """

        try:
            c = conn.cursor()
            c.execute(get_service_names_sql)
            service_names = [row[0] for row in c.fetchall()]

            return service_names
        except Error as e:
            print(e)
            return []
    
    def getAllPrices(dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        get_all_prices = '''
                            SELECT p.PROD_ID, s.SERV_NAME, p.PROD_SZ, p.PROD_PRICE
                            FROM product p
                            JOIN service s ON p.SERV_ID = s.SERV_ID
                        '''
        try:
            c = conn.cursor()
            c.execute(get_all_prices)

            rows = c.fetchall()
            return rows
        except Error as e:
            print(e)
            return []
    
    def displayPrices(self, rows):
        self.ui.pricelist_table.setRowCount(0)

        for row in rows:
            rowPosition = self.ui.pricelist_table.rowCount()

            if rowPosition > row[0]:
                continue

            itemCount = 0

            self.ui.pricelist_table.setRowCount(rowPosition + 1)
            prices_tablewidgetitem = QTableWidgetItem()
            self.ui.pricelist_table.setVerticalHeaderItem(rowPosition, prices_tablewidgetitem)

            for idx, item in enumerate(row):
                if idx == 0:
                    display_item = "P-" + str(item)
                else:
                    display_item = str(item)

                self.prices_tablewidgetitem = QTableWidgetItem()
                self.ui.pricelist_table.setItem(rowPosition, itemCount, self.prices_tablewidgetitem)
                self.prices_tablewidgetitem = self.ui.pricelist_table.item(rowPosition, itemCount)
                self.prices_tablewidgetitem.setText(display_item)

                itemCount = itemCount + 1
            rowPosition = rowPosition + 1

    
    def addPrice(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        product_service = self.ui.cat_name_pricelist.currentText()
        product_size = self.ui.size_pricelist.text()
        product_price = self.ui.price_pricelist.text()

        if not product_size or not product_price:

# ================ PROMPT ================ #
            print("Missing fields.")
            return
        
        check_service_exists_sql = f"""
            SELECT SERV_ID FROM service WHERE SERV_NAME = '{product_service}';
        """

        c = conn.cursor()
        c.execute(check_service_exists_sql)
        serv_id_result = c.fetchone()

        if not serv_id_result:
# ================ PROMPT ================ #
            print("Service does not exist.")
            return

        serv_id = serv_id_result[0]

        check_price_exists_sql = f"""
                                    SELECT PROD_ID FROM product
                                    WHERE SERV_ID = '{serv_id}'
                                    AND PROD_SZ = '{product_size}'
                                    AND PROD_PRICE = '{product_price}';
                                    """
        c = conn.cursor()
        c.execute(check_price_exists_sql)
        existing_price = c.fetchone()

        if existing_price:
# ================ PROMPT ================ #
            print("Price for product already exists.")
            return


        insert_price_data_sql = f""" 
                                        INSERT INTO product (SERV_ID, PROD_SZ, PROD_PRICE) VALUES ('{serv_id}','{product_size}', '{product_price}'); 
                                    """

        try:
            c = conn.cursor()
            c.execute(insert_price_data_sql)
            conn.commit()

            self.ui.id_pricelist.setText('')
            self.ui.cat_name_pricelist.setCurrentIndex(0)
            self.ui.size_pricelist.setPlaceholderText('')
            self.ui.price_pricelist.setPlaceholderText('')
            self.ui.size_pricelist.setText('')
            self.ui.price_pricelist.setText('')

            DBQueries.displayPrices(self, DBQueries.getAllPrices(dbFolder))

        except Error as e:
            print(e)

    def editPrice(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        selected_row = self.ui.pricelist_table.currentRow()
        if selected_row < 0:
# ================ PROMPT ================ #
            print("No product selected.")
            return

        product_id = int(self.ui.pricelist_table.item(selected_row, 0).text().split('-')[-1])
        product_service = self.ui.cat_name_pricelist.currentText()
        product_size = self.ui.size_pricelist.text()
        product_price = self.ui.price_pricelist.text()

        get_price_data_sql = f"""
                                SELECT SERV_ID, PROD_SZ, PROD_PRICE FROM product
                                WHERE PROD_ID = {product_id};
                                """
        c = conn.cursor()
        c.execute(get_price_data_sql)
        existing_data = c.fetchone()

        if not product_service:
            product_service = existing_data[0]
        if not product_size:
            product_size = existing_data[1]
        if not product_price:
            product_price = existing_data[2]

        check_service_exists_sql = f"""
            SELECT SERV_ID FROM service WHERE SERV_NAME = '{product_service}';
        """

        c = conn.cursor()
        c.execute(check_service_exists_sql)
        serv_id_result = c.fetchone()

        if not serv_id_result:
# ================ PROMPT ================ #
            print("Service does not exist.")
            return

        serv_id = serv_id_result[0]

        check_price_exists_sql = f"""
                                    SELECT PROD_ID FROM product
                                    WHERE SERV_ID = '{serv_id}'
                                    AND PROD_SZ = '{product_size}'
                                    AND PROD_PRICE = '{product_price}';
                                    """
        c.execute(check_price_exists_sql)
        existing_price = c.fetchone()

        if existing_price:
# ================ PROMPT ================ #
            print("Product with updated values already exists in another row.")
            return

        if product_service == existing_data[0] and product_size == existing_data[1] and product_price == existing_data[2]:
# ================ PROMPT ================ #
            print("No changes made to the product details.")
            return

        update_price_data_sql = f""" 
                                        UPDATE product 
                                        SET SERV_ID = '{serv_id}', PROD_SZ = '{product_size}', PROD_PRICE = '{product_price}'
                                        WHERE PROD_ID = {product_id};
                                    """

        try:
            c = conn.cursor()
            c.execute(update_price_data_sql)
            conn.commit()
            
            self.ui.id_pricelist.setText('')
            self.ui.cat_name_pricelist.setCurrentIndex(0)
            self.ui.size_pricelist.setPlaceholderText('')
            self.ui.price_pricelist.setPlaceholderText('')
            self.ui.size_pricelist.setText('')
            self.ui.price_pricelist.setText('')

            DBQueries.displayPrices(self, DBQueries.getAllPrices(dbFolder))

        except Error as e:
            print(e)
    
    def deletePrice(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        selected_rows = self.ui.pricelist_table.selectionModel().selectedRows()
        if not selected_rows:
# ================ PROMPT ================ #
            print("No price for product selected.")
            return

        if len(selected_rows) == 1:
            prod_id = int(self.ui.pricelist_table.item(selected_rows[0].row(), 0).text().split('-')[-1])

            delete_price_sql = f"""
                                    DELETE FROM product
                                    WHERE PROD_ID = {prod_id};
                                """

            try:
                c = conn.cursor()
                c.execute(delete_price_sql)
                conn.commit()

                product_size = DBQueries.getProductSizes(dbFolder)
                self.ui.category_size.clear()
                self.ui.category_size.addItems(product_size)

                DBQueries.displayPrices(self, DBQueries.getAllPrices(dbFolder))

            except Error as e:
                print(e)

        else:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Question)
            message_box.setText("You have selected multiple products. Are you sure you want to delete them?")
            message_box.setWindowTitle("Confirm Deletion")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            message_box.setDefaultButton(QMessageBox.No)

            response = message_box.exec()

            if response == QMessageBox.Yes:
                prices_ids = [int(self.ui.pricelist_table.item(row.row(), 0).text().split('-')[-1]) for row in selected_rows]

                delete_selected_prices_sql = f"""
                                                DELETE FROM product
                                                WHERE PROD_ID IN ({', '.join(str(id) for id in prices_ids)});
                                            """

                try:
                    c = conn.cursor()
                    c.execute(delete_selected_prices_sql)
                    conn.commit()

                    product_size = DBQueries.getProductSizes(dbFolder)
                    self.ui.category_size.clear()
                    self.ui.category_size.addItems(product_size)

                    DBQueries.displayPrices(self, DBQueries.getAllPrices(dbFolder))

                except Error as e:
                    print(e)

    def on_price_selection_changed(self):
        selected_rows = self.ui.pricelist_table.selectionModel().selectedRows()
        add_item_pricelist_btn = self.ui.add_item_pricelist_btn
        update_pricelist_btn = self.ui.update_pricelist_btn

        if len(selected_rows) > 0:
            add_item_pricelist_btn.setVisible(False)
        else:
            add_item_pricelist_btn.setVisible(True)

        if len(selected_rows) > 1:
            update_pricelist_btn.setVisible(False)
        else:
            update_pricelist_btn.setVisible(True)

    #================================= PARTICULARS QUERIES ====================================#
    def getAllParticulars(dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        get_all_particular = """ SELECT * FROM particular; """

        try:
            c = conn.cursor()
            c.execute(get_all_particular)

            return c
        except Error as e:
            print(e)
    
    def addParticular(self, dbFolder, particular_name, particular_num):
        conn = DBQueries.create_connection(dbFolder)

        particular_name = self.ui.customer_name_nt.text()
        particular_cn = self.ui.contact_num_nt.text()

        if not particular_name or not particular_cn:
# ================ PROMPT ================ #
            print("Missing fields.")
            return
        
        insert_particular_data_sql = f""" 
                                        INSERT INTO particular (PRTCLR_NAME, PRTCLR_CN) VALUES ('{particular_name}','{particular_cn}'); 
                                    """

        try:
            c = conn.cursor()
            c.execute(insert_particular_data_sql)
            conn.commit()

            particular_name = self.ui.customer_name_nt.setText("")
            particular_cn = self.ui.contact_num_nt.setText("")

        except Error as e:
            print(e)

    #=============================== JOB QUERIES ==================================#
    def getProductSizes(self, dbFolder):
        selected_service = self.ui.category_name_nt.currentText()
        conn = DBQueries.create_connection(dbFolder)

        get_sizes_sql = f"""SELECT DISTINCT PROD_SZ
                            FROM product p
                            INNER JOIN service s ON p.SERV_ID = s.SERV_ID 
                            WHERE SERV_NAME = '{selected_service}';
                        """
        try:
            c = conn.cursor()
            c.execute(get_sizes_sql)
            sizes = [row[0] for row in c.fetchall()]

            self.ui.category_size.clear()
            if not sizes:
                self.ui.category_size.setPlaceholderText('No available sizes')
            else:
                if self.ui.category_size.count() > 0:
                    self.ui.category_size.setCurrentText(self.ui.category_size.itemText(0))
                self.ui.category_size.addItems(sizes)

            return sizes
        except Error as e:
            print(e)
            return []
         
    def getAllJobs(dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        check_job_temp_table_sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='job_temp';"
        c = conn.cursor()
        c.execute(check_job_temp_table_sql)
        job_temp_exists = c.fetchone()

        if job_temp_exists:
            get_all_jobs = """SELECT JOB_ID, SERV_NAME, PROD_SZ, PROD_PRICE, JOB_QTY, JOB_TOT
                            FROM job_temp
                            INNER JOIN product ON job_temp.PROD_ID = product.PROD_ID
                            INNER JOIN service ON product.SERV_ID = service.SERV_ID;
                        """
        else:
            return []

        try:
            c.execute(get_all_jobs)
            rows = c.fetchall()
            return rows

        except Error as e:
            print(e)
    
    def displayJobs(self, rows):
        self.ui.order_detail_table.setRowCount(0)

        for row in rows:
            rowPosition = self.ui.order_detail_table.rowCount()
            self.ui.order_detail_table.setRowCount(rowPosition + 1)

            for itemCount, item in enumerate(row[1:], start=0):
                order_tablewidgetitem = QTableWidgetItem(str(item))
                self.ui.order_detail_table.setItem(rowPosition, itemCount, order_tablewidgetitem)

    def create_job_temp_table(dbFolder):
        conn = DBQueries.create_connection(dbFolder)
        create_table_sql =  """
                                CREATE TABLE IF NOT EXISTS job_temp (
                                    JOB_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    PROD_ID INTEGER NOT NULL,
                                    JOB_QTY INTEGER NOT NULL,
                                    JOB_TOT REAL NOT NULL,
                                    SUBTOTAL REAL NOT NULL DEFAULT JOB_TOT,
                                    FOREIGN KEY (PROD_ID) REFERENCES product (PROD_ID));
                            """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
            conn.commit()
        except Error as e:
            print(e)
        
    def addJob(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)
        DBQueries.create_job_temp_table(dbFolder)

        job_service = self.ui.category_name_nt.currentText()
        job_size = self.ui.category_size.currentText()
        job_quantity = self.ui.product_quantity.currentText()

        if not job_service or not job_size or not job_quantity:
            print("Missing fields.")
            return

        get_job_price_sql = """ SELECT PROD_ID, PROD_PRICE FROM product p 
                                INNER JOIN service s ON s.SERV_ID = p.SERV_ID 
                                WHERE SERV_NAME = ? AND PROD_SZ = ?;
                            """
        try:
            c = conn.cursor()
            c.execute(get_job_price_sql, (job_service, job_size))
            product_data = c.fetchone()

            if not product_data:
                print("Price not found for the selected service and size.")
                return

            product_id, job_price = product_data

            job_total = job_price * int(job_quantity)

            check_job_sql = """
                        SELECT JOB_ID FROM job_temp WHERE PROD_ID = ? AND JOB_QTY = ?;
                        """
            c.execute(check_job_sql, (product_id, job_quantity))
            existing_job_id = c.fetchone()

            if existing_job_id:
                print("Similar job already exists.")
                return

            insert_job_data_sql = """
                INSERT INTO job_temp (PROD_ID, JOB_QTY, JOB_TOT, SUBTOTAL) VALUES (?, ?, ?, ?);
            """
            c.execute(insert_job_data_sql, (product_id, job_quantity, job_total, job_total))
            conn.commit()

            update_subtotal_sql = """
                UPDATE job_temp SET SUBTOTAL = (
                    SELECT IFNULL(SUM(JOB_TOT), 0) FROM job_temp
                );
            """
            c.execute(update_subtotal_sql)
            conn.commit()

            get_last_row_subtotal_sql = """
                                            SELECT SUBTOTAL FROM job_temp WHERE JOB_ID = (SELECT MAX(JOB_ID) FROM job_temp);
                                        """
            c.execute(get_last_row_subtotal_sql)
            last_row_subtotal = c.fetchone()[0]

            self.ui.subtotal_nt.setText(str(last_row_subtotal))

            self.ui.category_name_nt.setCurrentIndex(0)
            self.ui.category_size.setCurrentIndex(0)
            self.ui.product_quantity.setCurrentIndex(0)

            DBQueries.displayJobs(self, DBQueries.getAllJobs(dbFolder))

        except Error as e:
            print(e)

    def calculate_subtotal_from_job_temp(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        try:
            c = conn.cursor()

            get_subtotal_sql = """
                SELECT SUM(JOB_TOT) FROM job_temp;
            """
            c.execute(get_subtotal_sql)
            subtotal = c.fetchone()[0]

        except Error as e:
            print(e)
            subtotal = 0.0

        conn.close()

        return subtotal
    
    def transfer_data_from_job_temp_to_jobs(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        transfer_data_sql = """
            INSERT INTO jobs (PROD_ID, JOB_QTY, JOB_TOT)
            SELECT PROD_ID, JOB_QTY, JOB_TOT FROM job_temp;
        """
            
        try:
            c = conn.cursor()
            c.execute(transfer_data_sql)
            conn.commit()

            clear_job_temp_sql = "DROP TABLE job_temp;"
            c.execute(clear_job_temp_sql)
            conn.commit()

            DBQueries.displayJobs(self, DBQueries.getAllJobs(dbFolder))

        except Error as e:
            print(e)
    
    def deleteJob(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        all_jobs = DBQueries.getAllJobs(dbFolder)

        try:
            c = conn.cursor()
            for row in all_jobs:
                job_id = row[0]
                job_service = row[1]
                job_size = row[2]
                job_price = float(row[3])
                job_quantity = int(row[4])

                print(job_id)

                update_subtotal_sql = """
                                        UPDATE job_temp SET SUBTOTAL = (
                                            SELECT IFNULL(SUM(JOB_TOT), 0) FROM job_temp
                                        ) WHERE JOB_ID = (SELECT MAX(JOB_ID) FROM job_temp);
                                    """
                c.execute(update_subtotal_sql, (job_price * job_quantity, job_id))
                conn.commit()

                delete_job_sql = f"""
                                    DELETE FROM jobs
                                    WHERE JOB_ID = {job_id} IN (
                                        SELECT product.PROD_SZ, product.PROD_PRICE, jobs.JOB_QTY
                                        FROM jobs
                                        INNER JOIN product ON jobs.PROD_ID = product.PROD_ID
                                        INNER JOIN service ON product.SERV_ID = service.SERV_ID
                                        WHERE SERV_NAME = ? AND PROD_SZ = ? AND PROD_PRICE = ? AND JOB_QTY = ?);
                                """
                c.execute(delete_job_sql, (job_service, job_size, job_price, job_quantity))

            conn.commit()
            DBQueries.displayJobs(self, DBQueries.getAllJobs(dbFolder))

        except Error as e:
            print(e)
    
    def on_job_selection_changed(self):
        selected_rows = self.ui.order_detail_table.selectionModel().selectedRows()
        add_order_nt = self.ui.add_order_nt

        if len(selected_rows) > 0:
            add_order_nt.setVisible(False)
        else:
            add_order_nt.setVisible(True)
    #============================== PAYMENT QUERIES =================================#
    
    def addPayment(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        check_job_temp_table_sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='job_temp';"
        c = conn.cursor()
        c.execute(check_job_temp_table_sql)
        job_temp_exists = c.fetchone()

        if not job_temp_exists:
            print("Job list is empty. Please add jobs first.")
            return False

        pmt_disc_qlabel_text = self.ui.discount_nt.text()
        try:
            payment_discount = float(pmt_disc_qlabel_text) if pmt_disc_qlabel_text else 0.0
        except ValueError:
            print("Invalid discount amount.")
            return False

        subtotal = DBQueries.calculate_subtotal_from_job_temp(self, dbFolder)
        self.ui.subtotal_nt.setText(str(subtotal))

        if not DBQueries.checkDiscount(self, dbFolder):
                return False

        payment_total = subtotal - payment_discount
        self.ui.total_amount.setText(str(payment_total))

        payment_paid_text = self.ui.payment_nt.text()
        try:
            payment_paid = float(payment_paid_text)
        except ValueError:
            print("Invalid payment amount.")
            return False

        if not payment_paid or payment_paid < 0:
            print("Missing payment details or invalid payment amount.")
            return False

        payment_bal = payment_total - payment_paid
        payment_sts = 'Fully Paid' if payment_bal == 0 else 'Partially Paid'
        payment_date = datetime.now().strftime('%Y-%m-%d')

        insert_payment_sql = """
            INSERT INTO payment (PMT_DISC, PMT_TOT, PMT_PAID, PMT_BAL, PMT_DATE, PMT_STS)
            VALUES (?, ?, ?, ?, ?, ?);
        """

        try:
            c = conn.cursor()
            c.execute(insert_payment_sql, (payment_discount, payment_total, payment_paid, payment_bal, payment_date, payment_sts))
            conn.commit()

            print("Payment added successfully.")
            return True
        except Error as e:
            print("Error adding payment:", e)
            return False
        
    def checkDiscount(self, dbFolder):
        subtotal = DBQueries.calculate_subtotal_from_job_temp(self, dbFolder)
        pmt_disc_qlabel_text = self.ui.discount_nt.text()

        if subtotal is None:
            print("Subtotal is not available. Please add jobs first.")
            return False

        try:
            payment_discount = float(pmt_disc_qlabel_text) if pmt_disc_qlabel_text else 0.0
        except ValueError:
            print("Invalid discount amount.")
            return False

        if payment_discount > subtotal:
            QMessageBox.warning(self, "Invalid Discount", "Discount amount cannot be greater than the subtotal.")
            return False

        return True
    #============================= TRANSACTION QUERIES ==============================#
    def getAllTransactions(dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        get_all_transactions = """ SELECT * FROM transactions; """

        try:
            c = conn.cursor()
            c.execute(get_all_transactions)

            return c
        except Error as e:
            print(e)

