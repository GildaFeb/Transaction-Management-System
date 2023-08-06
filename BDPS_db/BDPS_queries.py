import sqlite3
from sqlite3 import Error
from datetime import datetime

from PyQt5 import QtWidgets, QtSql
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

from openpyxl import load_workbook




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

    #===========================================================================================================#
    #                                           SERVICE QUERIES                                                 #
    #===========================================================================================================#
    def getAllServices(dbFolder):
        conn = None
        try:
            conn = sqlite3.connect(dbFolder)
            c = conn.cursor()

            get_all_service = """ SELECT * FROM service; """
            c.execute(get_all_service)

            return c.fetchall()

        except sqlite3.Error as e:
            print("Error executing query:", e)

        finally:
            if c:
                c.close()
            if conn:
                conn.close()

        return []

    def displayServices(self, rows):
        self.ui.pricelist_table.setRowCount(0)

        for rowPosition, row in enumerate(rows):
            display_row = ["S-" + str(row[0])] + [str(item) for item in row[1:]]
            self.ui.category_table.setRowCount(rowPosition + 1)

            for column_index, item in enumerate(display_row):
                services_tablewidgetitem = QTableWidgetItem(item)
                self.ui.category_table.setItem(rowPosition, column_index, services_tablewidgetitem)

    def resetService(self, dbFolder):
        self.ui.id_category.clear()
        self.ui.product_name_category.setText("")
        self.ui.category_description.setText("")
        self.ui.product_name_category.setPlaceholderText("")
        self.ui.category_description.setPlaceholderText("")
        self.ui.status_category.setCurrentIndex(0)

        service_names = DBQueries.getServiceNames(dbFolder)
        self.ui.cat_name_pricelist.clear()
        self.ui.cat_name_pricelist.addItems(service_names)
        self.ui.category_name_nt.clear()
        self.ui.category_name_nt.addItems(service_names)


    def addService(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        service_name = self.ui.product_name_category.text()
        service_desc = self.ui.category_description.text()
        service_sts = self.ui.status_category.currentText()

        if not service_name or not service_desc or not service_sts:
            QMessageBox.warning(self, "Warning", "Please fill up all the fields with the correct data.")
            return

        check_service_exists_sql = """
            SELECT SERV_ID FROM service
            WHERE SERV_NAME = ?;
        """
        c = conn.cursor()
        c.execute(check_service_exists_sql, (service_name, ))
        existing_service = c.fetchone()

        if existing_service:
            QMessageBox.warning(self, "Warning", "Service already exists.")
            return

        else:
            insert_service_data_sql = """
            INSERT INTO service (SERV_NAME, SERV_DESC, SERV_STS) VALUES (?, ?, ?);
            """
            QMessageBox.about(self, "Message", "Service successfully added.")

        try:
            c.execute(insert_service_data_sql, (service_name, service_desc, service_sts))
            conn.commit()
            conn.close()

            DBQueries.resetService(self, dbFolder)
            DBQueries.displayServices(self, DBQueries.getAllServices(dbFolder))

        except Error as e:
            print(e)
            QMessageBox.about(self, "Error", "An error occurred while adding the service.")

    def editService(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        selected_row = self.ui.category_table.currentRow()
        if selected_row < 0:
            QMessageBox.about(self, "Message", "Please select a row to edit.")
            return

        service_id = int(self.ui.category_table.item(selected_row, 0).text().split('-')[-1])
        service_name = self.ui.product_name_category.text()
        service_desc = self.ui.category_description.text()
        service_sts = self.ui.status_category.currentText()

        get_service_data_sql = """
            SELECT SERV_NAME, SERV_DESC, SERV_STS FROM service
            WHERE SERV_ID = ?;
        """
        c = conn.cursor()
        c.execute(get_service_data_sql, (service_id,))
        existing_data = c.fetchone()

        if not service_name:
            service_name = existing_data[0]
        if not service_desc:
            service_desc = existing_data[1]
        if not service_sts:
            service_sts = existing_data[2]

        check_service_exists_sql = """
            SELECT SERV_ID FROM service
            WHERE SERV_NAME = ? AND SERV_DESC = ? AND SERV_STS = ?
            AND SERV_ID != ?;
        """
        c.execute(check_service_exists_sql, (service_name, service_desc, service_sts, service_id))
        existing_service = c.fetchone()

        if existing_service:
            QMessageBox.about(self, "Message", "Service with updated values already exists in another row.")
            return

        if service_name == existing_data[0] or service_desc == existing_data[1] or service_sts == existing_data[2]:
            QMessageBox.about(self, "Message", "No changes made to the service details.")
            return
        
        update_service_data_sql = """
            UPDATE service
            SET SERV_NAME = ?, SERV_DESC = ?, SERV_STS = ?
            WHERE SERV_ID = ?;
        """

        try:
            c.execute(update_service_data_sql, (service_name, service_desc, service_sts, service_id))
            conn.commit()
            conn.close()

            DBQueries.resetService(self, dbFolder)
            DBQueries.displayServices(self, DBQueries.getAllServices(dbFolder))

            QMessageBox.about(self, "Message", "Service details updated successfully.")
        except Error as e:
            print(e)
            QMessageBox.about(self, "Error", "An error occurred while updating the service details.")

    def deleteService(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        selected_rows = self.ui.category_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.about(self, "Message", "Please select row/s to delete.")
            return

        c = conn.cursor()
        DBQueries.resetService(self, dbFolder)

        if len(selected_rows) == 1:
            service_id = int(self.ui.category_table.item(selected_rows[0].row(), 0).text().split('-')[-1])

            delete_service_sql = """
                DELETE FROM service
                WHERE SERV_ID = ?;
            """

            try:
                c.execute(delete_service_sql, (service_id,))
                conn.commit()
                conn.close()

                DBQueries.resetService(self, dbFolder)
                DBQueries.displayServices(self, DBQueries.getAllServices(dbFolder))

                QMessageBox.about(self, "Message", "Service deleted successfully.")
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

                delete_selected_service_sql = """
                    DELETE FROM service
                    WHERE SERV_ID IN ({});
                """.format(', '.join('?' for _ in service_ids))

                try:
                    c.execute(delete_selected_service_sql, service_ids)
                    conn.commit()
                    conn.close()

                    DBQueries.resetService(self, dbFolder)
                    DBQueries.displayServices(self, DBQueries.getAllServices(dbFolder))

                    QMessageBox.about(self, "Message", "Selected services deleted successfully.")
                except Error as e:
                    print(e)

    def on_service_selection_changed(self):
        selected_rows = self.ui.category_table.selectionModel().selectedRows()
        add_btn = self.ui.add_category_btn
        edit_btn = self.ui.edit_category_btn

        add_btn.setVisible(len(selected_rows) == 0)
        edit_btn.setVisible(len(selected_rows) <= 1)

    #===========================================================================================================#
    #                                        PRICE LIST QUERIES                                                 #
    #===========================================================================================================#
    def getServiceNames(dbFolder):
        try:
            conn = sqlite3.connect(dbFolder)
            c = conn.cursor()

            get_service_names_sql = """SELECT SERV_NAME
                                    FROM service
                                    WHERE SERV_STS = ?;
                                """

            c.execute(get_service_names_sql, ('Available',))
            service_names = [row[0] for row in c.fetchall()]
            conn.close()

            return service_names
        except sqlite3.Error as e:
            print("Error:", e)
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
            c.close()

            return rows
        except Error as e:
            print(e)
            return []
    
    def displayPrices(self, rows):
        self.ui.pricelist_table.setRowCount(0)

        for rowPosition, row in enumerate(rows):
            display_row = ["P-" + str(row[0])] + [str(item) for item in row[1:]]
            self.ui.pricelist_table.setRowCount(rowPosition + 1)

            for column_index, item in enumerate(display_row):
                prices_tablewidgetitem = QTableWidgetItem(item)
                self.ui.pricelist_table.setItem(rowPosition, column_index, prices_tablewidgetitem)

    def resetPrices(self):
        self.ui.id_pricelist.clear()
        self.ui.cat_name_pricelist.setCurrentIndex(0)
        self.ui.size_pricelist.clear()
        self.ui.size_pricelist.setPlaceholderText('')
        self.ui.price_pricelist.setSpecialValueText("0.00")

    def addPrice(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        product_service = self.ui.cat_name_pricelist.currentText()
        product_size = self.ui.size_pricelist.text()
        product_price = self.ui.price_pricelist.value()

        if not product_size or not product_price:
            QMessageBox.warning(self, "Warning", "Please fill up all the fields with the correct data")
            return

        try:
                c = conn.cursor()

                get_serv_id_sql = "SELECT SERV_ID FROM service WHERE SERV_NAME = ?;"
                c.execute(get_serv_id_sql, (product_service,))
                serv_id_result = c.fetchone()

                if not serv_id_result:
                    QMessageBox.about(self, "Message", "Service not found. Please click at least one row.")
                    return

                serv_id = serv_id_result[0]

                check_price_exists_sql = """
                    SELECT PROD_ID FROM product
                    WHERE SERV_ID = ? AND PROD_SZ = ? AND PROD_PRICE = ?;
                """
                c.execute(check_price_exists_sql, (serv_id, product_size, product_price))
                existing_price = c.fetchone()

                if existing_price:
                    QMessageBox.about(self, "Message", "Price for product already exists.")
                else:
                    insert_price_data_sql = """ 
                        INSERT INTO product (SERV_ID, PROD_SZ, PROD_PRICE) VALUES (?, ?, ?);
                    """
                    c.execute(insert_price_data_sql, (serv_id, product_size, product_price))
                    conn.commit()

                    DBQueries.resetPrices(self)
                    DBQueries.displayPrices(self, DBQueries.getAllPrices(dbFolder))

                    QMessageBox.about(self, "Message", "Product successfully added.")

        except sqlite3.Error as e:
            print("Error while executing the query:", e)
            QMessageBox.critical(self, "Error", "An error occurred while adding the price. Please try again later.")

    def editPrice(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        selected_row = self.ui.pricelist_table.currentRow()
        if selected_row < 0:
            QMessageBox.about(self, "Message", "No product selected")
            return

        product_id = int(self.ui.pricelist_table.item(selected_row, 0).text().split('-')[-1])
        product_service = self.ui.cat_name_pricelist.currentText()
        product_size = self.ui.size_pricelist.text()
        product_price = self.ui.price_pricelist.value()

        get_price_data_sql = "SELECT SERV_ID, PROD_SZ, PROD_PRICE FROM product WHERE PROD_ID = ?;"
        c = conn.cursor()
        c.execute(get_price_data_sql, (product_id,))
        existing_data = c.fetchone()

        if existing_data:
            if not product_service:
                product_service = existing_data[0]
            if not product_size:
                product_size = existing_data[1]
            if not product_price:
                product_price = existing_data[2]

        check_service_exists_sql = "SELECT SERV_ID FROM service WHERE SERV_NAME = ?;"
        c.execute(check_service_exists_sql, (product_service,))
        serv_id_result = c.fetchone()

        if not serv_id_result:
            QMessageBox.about(self, "Message", "Service does not exist")
            return

        serv_id = serv_id_result[0]

        check_price_exists_sql = """
            SELECT PROD_ID FROM product
            WHERE SERV_ID = ? AND PROD_SZ = ? AND PROD_PRICE = ?;
        """
        c.execute(check_price_exists_sql, (serv_id, product_size, product_price))
        existing_price = c.fetchone()

        if existing_price:
            QMessageBox.about(self, "Message", "Product with updated values already exists")
            return

        if product_service == existing_data[0] and product_size == existing_data[1] and product_price == existing_data[2]:
            QMessageBox.about(self, "Message", "No changes made to the product details.")
            return

        update_price_data_sql = """
            UPDATE product
            SET SERV_ID = ?, PROD_SZ = ?, PROD_PRICE = ?
            WHERE PROD_ID = ?;
        """
        try:
            c = conn.cursor()
            c.execute(update_price_data_sql, (serv_id, product_size, product_price, product_id))
            conn.commit()
            conn.close()

            DBQueries.resetPrices(self)
            DBQueries.displayPrices(self, DBQueries.getAllPrices(dbFolder))

        except Error as e:
            print(e)
    
    def deletePrice(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        selected_rows = self.ui.pricelist_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.about(self, "Message", "No price for selected product")
            return

        if len(selected_rows) == 1:
            prod_id = int(self.ui.pricelist_table.item(selected_rows[0].row(), 0).text().split('-')[-1])

            delete_price_sql = """
                DELETE FROM product
                WHERE PROD_ID = ?;
            """

            try:
                c = conn.cursor()
                c.execute(delete_price_sql, (prod_id,))
                conn.commit()

                product_size = DBQueries.getProductSizes(self, dbFolder)
                self.ui.category_size.clear()
                self.ui.category_size.addItems(product_size)

                DBQueries.resetPrices(self)
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

                delete_selected_prices_sql = """
                    DELETE FROM product
                    WHERE PROD_ID IN ({});
                """.format(', '.join('?' for _ in prices_ids))

                try:
                    c = conn.cursor()
                    c.execute(delete_selected_prices_sql, prices_ids)
                    conn.commit()

                    product_size = DBQueries.getProductSizes(dbFolder)
                    self.ui.category_size.clear()
                    self.ui.category_size.addItems(product_size)

                    DBQueries.resetService(self, dbFolder)
                    DBQueries.displayPrices(self, DBQueries.getAllPrices(dbFolder))

                except Error as e:
                    print(e)

    def on_price_selection_changed(self):
        selected_rows = self.ui.pricelist_table.selectionModel().selectedRows()
        add_item_pricelist_btn = self.ui.add_item_pricelist_btn
        update_pricelist_btn = self.ui.update_pricelist_btn

        add_item_pricelist_btn.setVisible(len(selected_rows) == 0)
        update_pricelist_btn.setVisible(len(selected_rows) <= 1)

    #===========================================================================================================#
    #                                       PARTICULARS QUERIES                                                 #
    #===========================================================================================================#
    def getAllParticulars(dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        get_all_particular = """ SELECT * FROM particular; """

        try:
            c = conn.cursor()
            c.execute(get_all_particular)

            rows = c.fetchall()

            return rows
        except Error as e:
            print(e)
            return None
    
    def addParticular(self, dbFolder, particular_name, particular_cn):
        conn = DBQueries.create_connection(dbFolder)

        insert_particular_data_sql = """
            INSERT INTO particular (PRTCLR_NAME, PRTCLR_CN) VALUES (?, ?);
        """

        try:
            c = conn.cursor()
            c.execute(insert_particular_data_sql, (particular_name, particular_cn))
            conn.commit()

            self.ui.customer_name_nt.clear()
            self.ui.contact_num_nt.clear()

        except Error as e:
            print(e)

    #===========================================================================================================#
    #                                             JOB QUERIES                                                   #
    #===========================================================================================================#
    def getProductSizes(self, dbFolder):
        selected_service = self.ui.category_name_nt.currentText()
        conn = DBQueries.create_connection(dbFolder)

        get_sizes_sql = """SELECT DISTINCT PROD_SZ
                  FROM product p
                  INNER JOIN service s ON p.SERV_ID = s.SERV_ID 
                  WHERE SERV_NAME = ?;
               """
        try:
            c = conn.cursor()
            c.execute(get_sizes_sql, (selected_service,))
            sizes = [row[0] for row in c.fetchall()]

            self.ui.category_size.clear()
            if not sizes:
                self.ui.service_size_error.setText("No available sizes.")
                self.ui.service_size_error.setStyleSheet('font-size: 3rem')
                
            else:
                if self.ui.category_size.count() > 0:
                    self.ui.category_size.setCurrentText(self.ui.category_size.itemText(0))
                self.ui.category_size.addItems(sizes)
                self.ui.service_size_error.setText("")
                self.ui.service_size_error.setStyleSheet('font-size: 0rem')
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

            for itemCount, item in enumerate(row[0:], start=0):
                order_tablewidgetitem = QTableWidgetItem(str(item))
                self.ui.order_detail_table.setItem(rowPosition, itemCount, order_tablewidgetitem)

    def create_job_temp_table(dbFolder):
        conn = DBQueries.create_connection(dbFolder)
        create_table_sql =  """
                                CREATE TABLE IF NOT EXISTS job_temp (
                                    JOB_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                    PROD_ID INTEGER NOT NULL,
                                    JOB_QTY INTEGER DEFAULT NULL,
                                    JOB_TOT NUMERIC(10, 2) DEFAULT NULL,
                                    SUBTOTAL NUMERIC(10, 2) DEFAULT NULL,
                                    TXN_CODE INTEGER DEFAULT NULL,
                                    FOREIGN KEY (PROD_ID) REFERENCES product (PROD_ID),
                                    FOREIGN KEY (TXN_CODE) REFERENCES transactions(TXN_CODE));
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
        job_quantity = self.ui.product_quantity.value()

        if not job_service or not job_size or not job_quantity:
            QMessageBox.about(self, "Message", "Please fill up all the forms with correct data")
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
                QMessageBox.about(self, "Message", "Price not found for the selected service and size")
                return

            product_id, job_price = product_data

            job_total = job_price * int(job_quantity)

            check_job_sql = """
                        SELECT JOB_ID FROM job_temp WHERE PROD_ID = ? AND JOB_QTY = ?;
                        """
            c.execute(check_job_sql, (product_id, job_quantity))
            existing_job_id = c.fetchone()

            if existing_job_id:
                QMessageBox.about(self, "Message", "Similar job exists")
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
            self.ui.product_quantity.setValue(0)

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
    
    def resetJobDetails(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        try:
            c = conn.cursor()

            clear_job_temp_sql = "DROP TABLE job_temp;"
            c.execute(clear_job_temp_sql)
            conn.commit()

            DBQueries.displayJobs(self, DBQueries.getAllJobs(dbFolder))

        except Error as e:
            print(e)
    
    def resetPayment(self, dbFolder):
        total_subtotal = DBQueries.calculate_subtotal_from_job_temp(self, dbFolder)

        if total_subtotal is not None:
            self.ui.subtotal_nt.setText(str(total_subtotal))

            new_subtotal = self.ui.subtotal_nt.text().strip()
            new_discount = self.ui.discount_nt.text().strip()

            try:
                subtotal_value = float(new_subtotal)
            except ValueError:
                subtotal_value = 0.0

            try:
                discount_value = float(new_discount)
            except ValueError:
                discount_value = 0.0

            total_amount = subtotal_value - discount_value
            self.ui.total_nt.setText(str(total_amount))

            if self.ui.total_nt.text().strip() and new_discount:
                try:
                    total_value = float(self.ui.total_nt.text().strip())
                    payment_paid_value = float(self.ui.payment_nt.text().strip())

                    if total_value and payment_paid_value:
                        balance = total_value - payment_paid_value
                        self.ui.balance_nt.setText(str(balance))
                    else:
                        self.ui.balance_nt.clear()
                except ValueError:
                    self.ui.balance_nt.clear()
            else:
                self.ui.balance_nt.clear()
        else:
            self.ui.total_nt.clear()

    def deleteJob(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        selected_rows = self.ui.order_detail_table.selectionModel().selectedRows()

        if len(selected_rows) == 1:
            job_count = int(self.ui.order_detail_table.item(selected_rows[0].row(), 0).text())

            delete_service_sql = f"""
                                    DELETE FROM job_temp
                                    WHERE JOB_ID = {job_count};
                                """

            try:
                c = conn.cursor()
                c.execute(delete_service_sql)
                conn.commit()
                
                DBQueries.resetPayment(self, dbFolder)
                DBQueries.displayJobs(self, DBQueries.getAllJobs(dbFolder))

            except Error as e:
                print(e)

        else:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Question)
            message_box.setText("You have selected multiple jobs. Are you sure you want to delete them?")
            message_box.setWindowTitle("Confirm Deletion")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            message_box.setDefaultButton(QMessageBox.No)

            response = message_box.exec()

            if response == QMessageBox.Yes:
                job_ids = [int(self.ui.order_detail_table.item(row.row(), 0).text()) for row in selected_rows]

                delete_selected_job_sql = f"""
                                                DELETE FROM job_temp
                                                WHERE JOB_ID IN ({', '.join(str(id) for id in job_ids)});
                                            """

                try:
                    c = conn.cursor()
                    c.execute(delete_selected_job_sql)
                    conn.commit()

                    DBQueries.resetPayment(self, dbFolder)
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

    #===========================================================================================================#
    #                                          PAYMENT QUERIES                                                  #
    #===========================================================================================================#
    
    def addPayment(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        check_job_temp_table_sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='job_temp';"
        c = conn.cursor()
        c.execute(check_job_temp_table_sql)
        job_temp_exists = c.fetchone()

        if not job_temp_exists:
            QMessageBox.about(self, "Message", "Job lits is empty. Please add jobs first")
            return False

        pmt_disc_text = self.ui.discount_nt.text()
        try:
            payment_discount = float(pmt_disc_text) if pmt_disc_text else 0.0
        except ValueError:
            QMessageBox.about(self, "Message", "Invalid discount amount")
            return False

        subtotal = DBQueries.calculate_subtotal_from_job_temp(self, dbFolder)
        self.ui.subtotal_nt.setText(str(subtotal))

        if not DBQueries.checkDiscount(self, dbFolder):
                return False

        payment_total = subtotal - payment_discount
        self.ui.total_nt.setText(str(payment_total))

        payment_paid_text = self.ui.payment_nt.text()
        if not payment_paid_text.strip():
            payment_paid = 0.0
        else:
            try:
                payment_paid = float(payment_paid_text)
            except ValueError:
                QMessageBox.about(self, "Message", "Invalid payment amount")
                return False

        if not payment_paid or payment_paid < 0:
            QMessageBox.about(self, "Message", "Missing payment details or invalid payment amount")
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
            QMessageBox.about(self, "Message", "Payment added successfully")
            return True
        except Error as e:
            QMessageBox.about(self, "Error", "Error adding payment", e)
            return False
        
    def update_total_nt(self, dbFolder):
        subtotal = DBQueries.calculate_subtotal_from_job_temp(self, dbFolder)
        pmt_disc_text = self.ui.discount_nt.text()

        if subtotal is None:
            QMessageBox.about(self, "Message", "Subtotal is not available. Please add jobs first")
            return

        try:
            payment_discount = float(pmt_disc_text) if pmt_disc_text else 0.0
        except ValueError:
            QMessageBox.about(self, "Message", "Invalid discount amount.")
            return

        payment_total = subtotal - payment_discount
        self.ui.total_nt.setText(str(payment_total))
        
    def checkDiscount(self, dbFolder):
        subtotal = DBQueries.calculate_subtotal_from_job_temp(self, dbFolder)
        pmt_disc_text = self.ui.discount_nt.text()

        if subtotal is None:
            QMessageBox.about(self, "Message", "Please fill up all the forms with correct data")
            return False

        try:
            payment_discount = float(pmt_disc_text) if pmt_disc_text else 0.0
        except ValueError:
            QMessageBox.about(self, "Message", "Invalid discount amount")
            return False

        if payment_discount > subtotal:
            QMessageBox.warning(self, "Invalid Discount", "Discount amount cannot be greater than the subtotal.")
            self.ui.discount_nt.setText(str(subtotal))
            self.ui.discount_input.setValue(subtotal)

        return True
    
    def check_payment_amount(self, dbFolder):
        payment_nt = self.ui.payment_nt.text()
        total_nt = self.ui.total_nt.text()

        try:
            payment_nt_value = float(payment_nt) if payment_nt else 0.0
            total_nt_value = float(total_nt)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Invalid payment amount or total amount.")
            return

        if payment_nt_value > total_nt_value:
            warning_message = "Payment amount exceeds the total amount."
            QMessageBox.warning(self, "Invalid Payment Amount", warning_message)

            payment_nt_value -= (payment_nt_value - total_nt_value)
            self.ui.payment_nt.setText(str(payment_nt_value))

    def update_balance_nt(self, dbFolder):
        try:
            payment_nt_value = float(self.ui.payment_nt.text()) if self.ui.payment_nt.text() else 0.0
            total_nt_value = float(self.ui.total_nt.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Invalid payment amount or total amount.")
            return

        balance = total_nt_value - payment_nt_value
        self.ui.balance_nt.setText(str(balance))

    #===========================================================================================================#
    #                                       TRANSACTION QUERIES                                                 #
    #===========================================================================================================#
    def getAllTransactions(dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        get_all_transactions =  """ SELECT * FROM transactions
                                    INNER JOIN particular ON transactions.PRTCLR_ID = particular.PRTCLR_ID
                                    INNER JOIN payment ON transactions.TXN_CODE = payment.TXN_CODE
                                    INNER JOIN jobs job ON transactions.TXN_CODE = job.TXN_CODE
                                    INNER JOIN product ON job.PROD_ID = product.PROD_ID
                                    INNER JOIN service ON product.SERV_ID = service.SERV_ID;
                                """

        try:
            c = conn.cursor()
            c.execute(get_all_transactions)
            rows = c.fetchall()

            return rows
        except Error as e:
            print(e)

    def get_next_txn_code(self, dbFolder):
        conn = sqlite3.connect(dbFolder)
        cursor = conn.cursor()

        try:
            last_txn_code_query = "SELECT MAX(TXN_CODE) FROM transactions;"
            cursor.execute(last_txn_code_query)
            last_txn_code = cursor.fetchone()[0]

            current_txn_code = last_txn_code + 1 if last_txn_code else 1

            return current_txn_code

        except Exception as e:
            QMessageBox.warning(self, "Message", "Error retrieving next transaction code:", e)
            return None
        finally:
            cursor.close()
            conn.close()
    
    def displayTransactionRecords(self, rows):
        self.ui.transaction_record_tbl.setRowCount(0)
        displayed_txn_codes = set()

        for row in rows:
            txn_code = "T-" + str(row[0])

            if txn_code in displayed_txn_codes:
                continue

            displayed_txn_codes.add(txn_code)

            rowPosition = self.ui.transaction_record_tbl.rowCount()
            self.ui.transaction_record_tbl.setRowCount(rowPosition + 1)

            txn_date = row[2]
            particular_cn = row[5]
            pmt_tot = row[10]
            pmt_paid = row[11]
            txn_sts = row[3]
            pmt_sts = row[14]
            pmt_bal = row[12]

            self.ui.transaction_record_tbl.setItem(rowPosition, 0, QTableWidgetItem(str(txn_code)))
            self.ui.transaction_record_tbl.setItem(rowPosition, 1, QTableWidgetItem(str(txn_date)))
            self.ui.transaction_record_tbl.setItem(rowPosition, 2, QTableWidgetItem(str(particular_cn)))
            self.ui.transaction_record_tbl.setItem(rowPosition, 3, QTableWidgetItem(str(pmt_tot)))
            self.ui.transaction_record_tbl.setItem(rowPosition, 4, QTableWidgetItem(str(pmt_paid)))
            self.ui.transaction_record_tbl.setItem(rowPosition, 5, QTableWidgetItem(str(txn_sts)))
            self.ui.transaction_record_tbl.setItem(rowPosition, 6, QTableWidgetItem(str(pmt_sts)))
            self.ui.transaction_record_tbl.setItem(rowPosition, 7, QTableWidgetItem(str(pmt_bal)))

    def displayDailyTransactions(self, rows):
        self.ui.daily_tnx_table.setRowCount(0)

        for row in rows:
            rowPosition = self.ui.daily_tnx_table.rowCount()
            self.ui.daily_tnx_table.setRowCount(rowPosition + 1)

            job_id = "J-" + str(row[15])
            txn_date = row[2]
            prtclr_name = row[5]
            serv_name = row[2]
            prod_sz = row[22]
            job_qty = row[17]
            job_tot = row[18]

            self.ui.daily_tnx_table.setItem(rowPosition, 0, QTableWidgetItem(str(job_id)))
            self.ui.daily_tnx_table.setItem(rowPosition, 1, QTableWidgetItem(str(txn_date)))
            self.ui.daily_tnx_table.setItem(rowPosition, 2, QTableWidgetItem(str(prtclr_name)))
            self.ui.daily_tnx_table.setItem(rowPosition, 3, QTableWidgetItem(str(serv_name)))
            self.ui.daily_tnx_table.setItem(rowPosition, 4, QTableWidgetItem(str(prod_sz)))
            self.ui.daily_tnx_table.setItem(rowPosition, 5, QTableWidgetItem(str(job_qty)))
            self.ui.daily_tnx_table.setItem(rowPosition, 6, QTableWidgetItem(str(job_tot)))
    
    def displayDatewiseTransactions(self, rows):
        self.ui.datewise_transaction_table.setRowCount(0)
        displayed_txn_codes = set()

        for row in rows:
            txn_code = "T-" + str(row[0])
            
            if txn_code in displayed_txn_codes:
                continue
            
            displayed_txn_codes.add(txn_code)

            rowPosition = self.ui.datewise_transaction_table.rowCount()
            self.ui.datewise_transaction_table.setRowCount(rowPosition + 1)

            txn_date = row[2]
            particular_cn = row[5]
            pmt_tot = row[10]
            txn_sts = row[3]

            self.ui.datewise_transaction_table.setItem(rowPosition, 0, QTableWidgetItem(str(txn_code)))
            self.ui.datewise_transaction_table.setItem(rowPosition, 1, QTableWidgetItem(str(txn_date)))
            self.ui.datewise_transaction_table.setItem(rowPosition, 2, QTableWidgetItem(str(particular_cn)))
            self.ui.datewise_transaction_table.setItem(rowPosition, 3, QTableWidgetItem(str(pmt_tot)))
            self.ui.datewise_transaction_table.setItem(rowPosition, 4, QTableWidgetItem(str(txn_sts)))

    def displayDatewisePayments(self, rows):
        self.ui.datewise_payment_table.setRowCount(0)
        displayed_pmt_ids = set()

        for row in rows:
            pmt_id = "P-" + str(row[7])

            if pmt_id in displayed_pmt_ids:
                continue

            displayed_pmt_ids.add(pmt_id)

            rowPosition = self.ui.datewise_payment_table.rowCount()
            self.ui.datewise_payment_table.setRowCount(rowPosition + 1)

            pmt_date = row[13]
            prtclr_name = row[5]
            pmt_disc = row[9]
            pmt_tot = row[10]
            pmt_paid = row[11]
            pmt_bal = row[12]
            pmt_sts = row[14]

            self.ui.datewise_payment_table.setItem(rowPosition, 0, QTableWidgetItem(str(pmt_id)))
            self.ui.datewise_payment_table.setItem(rowPosition, 1, QTableWidgetItem(str(pmt_date)))
            self.ui.datewise_payment_table.setItem(rowPosition, 2, QTableWidgetItem(str(prtclr_name)))
            self.ui.datewise_payment_table.setItem(rowPosition, 3, QTableWidgetItem(str(pmt_disc)))
            self.ui.datewise_payment_table.setItem(rowPosition, 4, QTableWidgetItem(str(pmt_tot)))
            self.ui.datewise_payment_table.setItem(rowPosition, 5, QTableWidgetItem(str(pmt_paid)))
            self.ui.datewise_payment_table.setItem(rowPosition, 6, QTableWidgetItem(str(pmt_bal)))
            self.ui.datewise_payment_table.setItem(rowPosition, 7, QTableWidgetItem(str(pmt_sts)))

    def saveTransaction(self, dbFolder):
        prtclr_name = self.ui.customer_name_nt.text()
        prtclr_cn = self.ui.contact_num_nt.text()
        txn_date = self.ui.tnx_date_nt.date().toString('yyyy-MM-dd')
        txn_sts = self.ui.comboBox_2.currentText()
        pmt_disc = self.ui.discount_nt.text().strip()
        try:
            pmt_disc = float(pmt_disc) if pmt_disc else 0.0
        except ValueError:
            QMessageBox.warning(self, "Warning", "Invalid discount amount.")
            return False
        pmt_paid_text = self.ui.payment_nt.text().strip()
        if not pmt_paid_text:
            QMessageBox.warning(self, "Warning", "Payment amount is empty. Please enter a valid payment amount")
            return False

        try:
            pmt_paid = float(pmt_paid_text)
        except ValueError:
            QMessageBox.warning(self, "Message", "Invalid payment amount. Please enter a valid numeric value")
            return False

        conn = sqlite3.connect(dbFolder)
        cursor = conn.cursor()

        try:
            
            #========================== INSERT ON PARTICULAR ===========================#
            prtclr_insert_sql = """
                INSERT INTO particular (PRTCLR_NAME, PRTCLR_CN)
                VALUES (?, ?)
            """

            cursor.execute(prtclr_insert_sql, (prtclr_name, prtclr_cn))
            prtclr_id = cursor.lastrowid

            #========================== INSERT ON TRANSACTIONS ===========================#
            txn_insert_sql ="""
                INSERT INTO transactions (PRTCLR_ID, TXN_DATE, TXN_STS)
                VALUES (?, ?, ?)
            """

            current_prtclr_id = prtclr_id
            cursor.execute(txn_insert_sql, (current_prtclr_id, txn_date, txn_sts))

            #========================== INSERT ON JOBS ===========================#
            current_txn_code = DBQueries.get_next_txn_code(self, dbFolder)

            job_transfer_sql = """
                INSERT INTO jobs (PROD_ID, JOB_QTY, JOB_TOT, TXN_CODE)
                SELECT PROD_ID, JOB_QTY, JOB_TOT, ? FROM job_temp
            """
            cursor.execute(job_transfer_sql, (current_txn_code,))

            #========================== INSERT ON PAYMENT ===========================#
            pmt_tot = float(conn.execute("SELECT SUBTOTAL FROM job_temp WHERE JOB_ID = (SELECT MAX(JOB_ID) FROM job_temp)").fetchone()[0]) - pmt_disc
            pmt_bal = pmt_tot - pmt_paid
            pmt_sts = 'Fully Paid' if pmt_bal == 0 else 'Partially Paid'
            pmt_date = txn_date
            if pmt_bal != 0:
                txn_sts = 'Pending Transaction'
                QMessageBox.warning(self, "Message", "Remaining balance found. Setting to Pending...")

            pmt_insert_sql = """
                INSERT INTO payment (TXN_CODE, PMT_DISC, PMT_TOT, PMT_PAID, PMT_BAL, PMT_DATE, PMT_STS)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(pmt_insert_sql, (current_txn_code, pmt_disc, pmt_tot, pmt_paid, pmt_bal, pmt_date, pmt_sts))

            conn.commit()

            DBQueries.displayTransactionRecords(self, DBQueries.getAllTransactions(dbFolder))
            DBQueries.displayDailyTransactions(self, DBQueries.getAllTransactions(dbFolder))
            DBQueries.displayDatewiseTransactions(self, DBQueries.getAllTransactions(dbFolder))
            DBQueries.displayDatewisePayments(self, DBQueries.getAllTransactions(dbFolder))
            
            QMessageBox.about(self, "Message", "Transaction saved successfully.")

            self.ui.customer_name_nt.clear()
            self.ui.contact_num_nt.clear()
            self.ui.category_name_nt.setCurrentIndex(0)
            self.ui.category_size.setCurrentIndex(0)
            self.ui.product_quantity.setValue(0)
            self.ui.order_detail_table.clear()
            self.ui.order_detail_table.setRowCount(0)
            self.ui.subtotal_nt.setText("0.00")
            self.ui.discount_nt.setText("0.00")
            self.ui.discount_input.setValue(0)
            self.ui.payment_nt.setText("")
            self.ui.comboBox_2.setCurrentIndex(0)
            self.ui.balance_nt.setText('0.00')
            DBQueries.resetJobDetails(self, dbFolder)
            current_txn_code = DBQueries.get_next_txn_code(self, dbFolder)
            self.ui.tnx_code_nt.setText(str(current_txn_code))
            self.ui.total_nt.setText("0.00")


        except Exception as e:
            QMessageBox.warning(self, "Message", "An error occured.")
        finally:
            cursor.close()
            conn.close()

    def updateTransactions(self, dbFolder):
        
        conn = DBQueries.create_connection(dbFolder)
        c = conn.cursor()

        selected_row = self.ui.transaction_record_tbl.currentRow()

        txn_item = self.ui.transaction_record_tbl.item(selected_row, 0)
        txn_code = int(txn_item.text().split('-')[-1])

        self.ui.utd_id.setText("T-" + str(txn_code))

        self.ui.stackedWidget.setCurrentIndex(8)

        get_txn_jobs_data_sql = """
                                SELECT JOB_ID, SERV_NAME, PROD_SZ, PROD_PRICE, JOB_QTY, JOB_TOT FROM jobs j
                                INNER JOIN product p ON p.PROD_ID = j.PROD_ID
                                INNER JOIN service s ON s.SERV_ID = p.SERV_ID
                                WHERE TXN_CODE = ?;
                                """
        c.execute(get_txn_jobs_data_sql, (txn_code,))
        jobs_data = c.fetchall()

        self.ui.order_detail_table_2.setRowCount(len(jobs_data))
        for row_index, row_data in enumerate(jobs_data):
            for col_index, cell_value in enumerate(row_data):
                self.ui.order_detail_table_2.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(cell_value)))

        get_txn_pmts_data_sql = """
                                SELECT DISTINCT PMT_DATE, PMT_PAID, PMT_BAL FROM payment p
                                INNER JOIN transactions t ON t.TXN_CODE = p.TXN_CODE
                                WHERE t.TXN_CODE = ?
                                """
        c.execute(get_txn_pmts_data_sql, (txn_code,))
        pmts_data = c.fetchall()

        self.ui.order_detail_table_3.setRowCount(len(pmts_data))
        for row_index, row_data in enumerate(pmts_data):
            for col_index, cell_value in enumerate(row_data):
                self.ui.order_detail_table_3.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(cell_value)))

        get_statuses_data_sql = """
                                SELECT TXN_STS, PMT_STS FROM payment p
                                INNER JOIN transactions t ON t.TXN_CODE = p.TXN_CODE
                                WHERE t.TXN_CODE = ?
                                """
        c.execute(get_statuses_data_sql, (txn_code,))
        statuses_data = c.fetchall()

        txn_sts, pmt_sts = statuses_data[0]

        self.ui.lineEdit_3.setText(str(txn_sts))
        self.ui.lineEdit_4.setText(str(pmt_sts))

        get_prtclr_data_sql = """
                                SELECT PRTCLR_NAME, PRTCLR_CN FROM particular p
                                INNER JOIN transactions t ON t.PRTCLR_ID = p.PRTCLR_ID
                                WHERE t.TXN_CODE = ?
                                """
        c.execute(get_prtclr_data_sql, (txn_code,))
        statuses_data = c.fetchall()

        prtclr_name, prtclr_cn = statuses_data[0]

        self.ui.customer_name_utd.setText(str(prtclr_name))
        self.ui.contact_num_utd.setText(str(prtclr_cn))

        if pmt_sts == 'Fully Paid':
            self.ui.utd_payment.setEnabled(False)
        else:
            self.ui.utd_payment.setEnabled(True)

        self.ui.save_update.clicked.connect(lambda: DBQueries.on_save_update(self, dbFolder, txn_code))

    def on_save_update(self, dbFolder, txn_code):
        conn = DBQueries.create_connection(dbFolder)
        c = conn.cursor()

        txn_sts = self.ui.comboBox.currentText()

        try:
            if self.ui.utd_payment.isEnabled():
                try:
                    this_txn_pmt_paid = float(self.ui.utd_payment.text())
                except ValueError:
                    QMessageBox.warning(self, "Message", "Invalid payment amount. Please enter a valid numberic value")
                    return
    
            get_this_txn_pmt_data_sql = """
                SELECT t.TXN_CODE, PMT_DISC, PMT_TOT, PMT_PAID, PMT_BAL, PMT_DATE, PMT_STS FROM transactions t
                INNER JOIN payment p ON t.TXN_CODE = p.TXN_CODE
                WHERE t.TXN_CODE = ?;
            """
            c.execute(get_this_txn_pmt_data_sql, (txn_code,))
            statuses_data = c.fetchall()

            if not statuses_data:
                QMessageBox.warning(self, "Message", f"Transaction with TXN_CODE={txn_code} not found in the database.")
                conn.close()
                return

            txn_code, pmt_disc, pmt_tot, pmt_paid, pmt_bal, pmt_date, pmt_sts = statuses_data[0]
            get_cumulative_payment_sql = """
                SELECT SUM(PMT_PAID) FROM payment WHERE TXN_CODE = ?;
            """
            c.execute(get_cumulative_payment_sql, (txn_code,))
            cumulative_payment = c.fetchone()[0]
            print(cumulative_payment)
            if cumulative_payment is None:
                cumulative_payment = 0.0

            this_txn_pmt_tot = pmt_tot - cumulative_payment
            this_txn_pmt_date = datetime.now().strftime('%Y-%m-%d')

            this_txn_pmt_bal = this_txn_pmt_tot - this_txn_pmt_paid

            if pmt_sts == 'Fully Paid':
                QMessageBox.about(self, "Message", "Total amount already fulfilled.")
            elif pmt_sts == 'Partially Paid':
                if this_txn_pmt_paid < 0:
                    QMessageBox.warning(self, "Message", "Payment amount cannot be negative.")
                    conn.close()
                    return

                if this_txn_pmt_paid > this_txn_pmt_tot:
                    QMessageBox.warning(self, "Message", "Payment exceeds the remaining balance.")
                    conn.close()
                    return
                
                this_txn_pmt_sts = 'Fully Paid' if this_txn_pmt_bal == 0 else 'Partially Paid'

                cumulative_payment += this_txn_pmt_paid

                insert_new_payment_sql = """
                    INSERT INTO payment (TXN_CODE, PMT_DISC, PMT_TOT, PMT_PAID, PMT_BAL, PMT_DATE, PMT_STS)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                """
                c.execute(insert_new_payment_sql, (txn_code, pmt_disc, this_txn_pmt_tot, this_txn_pmt_paid, this_txn_pmt_bal, this_txn_pmt_date, this_txn_pmt_sts))
                conn.commit()
                
            #================================ UPDATE PARTICULAR =============================#
            new_prtclr_name = self.ui.customer_name_utd.text()
            new_prtclr_cn = self.ui.contact_num_utd.text()

            update_particular_sql = """
                    UPDATE particular
                    SET PRTCLR_NAME=?, PRTCLR_CN=?
                    WHERE PRTCLR_ID IN (
                        SELECT PRTCLR_ID
                        FROM transactions
                        WHERE TXN_CODE=?
                    );
                """
            c.execute(update_particular_sql, (new_prtclr_name, new_prtclr_cn, txn_code))

            #================================ UPDATE TXN_STS =============================#
            update_txn_status_sql = """
                    UPDATE transactions
                    SET TXN_STS=?
                    WHERE TXN_CODE=?
                """
            c.execute(update_txn_status_sql, (txn_sts, txn_code))

            conn.commit()

            self.ui.order_detail_table_2.clearContents()
            self.ui.order_detail_table_2.setRowCount(0)
            self.ui.order_detail_table_3.clearContents()
            self.ui.order_detail_table_3.setRowCount(0)
            DBQueries.displayTransactionRecords(self, DBQueries.getAllTransactions(dbFolder))
            DBQueries.displayDailyTransactions(self, DBQueries.getAllTransactions(dbFolder))
            DBQueries.displayDatewisePayments(self, DBQueries.getAllTransactions(dbFolder))
            DBQueries.displayDailyTransactions(self, DBQueries.getAllTransactions(dbFolder))

            self.ui.stackedWidget.setCurrentIndex(4)
            QMessageBox.about(self, "Message", "Payment updated successfully.")
            conn.close()

        except QtSql.QSqlError as e:
            QMessageBox.warning(self, "Error", f"An unexpected error occurred while updating transaction: {e.text()}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An unexpected error occurred while updating transaction: {str(e)}")

    def on_txn_selection_changed(self):
        selected_rows = self.ui.transaction_record_tbl.selectionModel().selectedRows()
        update_txn_btn = self.ui.update_transaction
            
        if len(selected_rows) > 1:
            update_txn_btn.setVisible(False)
        else:
            update_txn_btn.setVisible(True)

    #===========================================================================================================#
    #                                              ON EXIT                                                      #
    #===========================================================================================================#
    def drop_job_temp_table(dbFolder):
        try:
            conn = sqlite3.connect(dbFolder)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS job_temp;")
            conn.commit()
            print("job_temp table dropped.")
        except Exception as e:
            print("Error dropping job_temp table:", e)
        finally:
            cursor.close()
            conn.close()

