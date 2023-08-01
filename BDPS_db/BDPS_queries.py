import os
import sys
import sqlite3
from sqlite3 import Error

from PyQt5.QtWidgets import QTableWidgetItem

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
        create_category_table = """ CREATE TABLE IF NOT EXISTS categories (
                                                `CAT_ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                `CAT_NAME` VARCHAR(50) DEFAULT NULL,
                                                `CAT_DESC` VARCHAR(1000) DEFAULT NULL,
                                                `CAT_STS` VARCHAR(50) DEFAULT NULL
                                                );
                                        """
        conn = DBQueries.create_connection(dbFolder)

        if conn is not None:
            DBQueries.create_table(conn, create_category_table)
        else:
            #PROMPT
            print("Error! Cannot connect.")
        
        create_product_table = """ CREATE TABLE IF NOT EXISTS product (
                                                `PROD_ID` INTEGER PRIMARY KEY,
                                                `CAT_ID` INTEGER NOT NULL,
                                                `PROD_SZ` VARCHAR(100) DEFAULT NULL,
                                                `PROD_PRICE` INTEGER DEFAULT NULL,
                                                FOREIGN KEY (`CAT_ID`) REFERENCES `categories` (`CAT_ID`)
                                                );
                                """
        conn = DBQueries.create_connection(dbFolder)

        if conn is not None:
            DBQueries.create_table(conn, create_product_table)
        else:
            #PROMPT
            print("Error! Cannot connect.")
    

    #============================= CATEGORY QUERIES =======================================#
    def getAllCategories(dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        get_all_categories = """ SELECT * FROM categories; """

        try:
            c = conn.cursor()
            c.execute(get_all_categories)

            return c
        except Error as e:
            print(e)

    def displayCategories(self, rows):
        self.ui.category_table.setRowCount(0)

        for row in rows:
            rowPosition = self.ui.category_table.rowCount()

            if rowPosition > row[0]:
                continue

            itemCount = 0

            self.ui.category_table.setRowCount(rowPosition+1)
            qtablewidgetitem = QTableWidgetItem()
            self.ui.category_table.setVerticalHeaderItem(rowPosition, qtablewidgetitem)

            for item in row:
                self.qtablewidgetitem = QTableWidgetItem()
                self.ui.category_table.setItem(rowPosition, itemCount, self.qtablewidgetitem)
                self.qtablewidgetitem = self.ui.category_table.item(rowPosition, itemCount)
                self.qtablewidgetitem.setText(str(item))

                itemCount = itemCount+1
            rowPosition = rowPosition+1
    
    def addCategory(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        category_name = self.ui.product_name_category.text()
        category_desc = self.ui.category_description.toPlainText()
        category_sts = self.ui.status_category.currentText()

        if not category_name or not category_desc:
            #PROMPT
            print("Missing fields.")
            return

        check_category_exists_sql = f"""
                                    SELECT CAT_ID FROM categories
                                    WHERE CAT_NAME = '{category_name}'
                                    AND CAT_DESC = '{category_desc}'
                                    AND CAT_STS = '{category_sts}';
                                    """
        c = conn.cursor()
        c.execute(check_category_exists_sql)
        existing_category = c.fetchone()

        if existing_category:
            #PROMPT
            print("Category already exists.")
            return

        insert_category_data_sql = f""" 
                                        INSERT INTO categories (CAT_NAME, CAT_DESC, CAT_STS) VALUES ('{category_name}','{category_desc}', '{category_sts}'); 
                                    """

        try:
            c = conn.cursor()
            c.execute(insert_category_data_sql)
            conn.commit()

            self.ui.product_name_category.setText("")
            self.ui.category_description.setText("")
            self.ui.status_category.itemText(0)

            category_names = DBQueries.getCategoryNames(dbFolder)
            self.ui.cat_name_pricelist.clear()
            self.ui.cat_name_pricelist.addItems(category_names)

            DBQueries.displayCategories(self, DBQueries.getAllCategories(dbFolder))

        except Error as e:
            print(e)

    def editCategory(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        selected_row = self.ui.category_table.currentRow()
        if selected_row < 0:
            #PROMPT
            print("No category selected.")
            return

        category_id = int(self.ui.category_table.item(selected_row, 0).text())
        category_name = self.ui.product_name_category.text()
        category_desc = self.ui.category_description.toPlainText()
        category_sts = self.ui.status_category.itemText(0)

        get_category_data_sql = f"""
                                SELECT CAT_NAME, CAT_DESC, CAT_STS FROM categories
                                WHERE CAT_ID = {category_id};
                                """
        c = conn.cursor()
        c.execute(get_category_data_sql)
        existing_data = c.fetchone()

        if not category_name:
            category_name = existing_data[0]
        if not category_desc:
            category_desc = existing_data[1]
        if not category_sts:
            category_sts = existing_data[2]

        check_category_exists_sql = f"""
                                    SELECT CAT_ID FROM categories
                                    WHERE CAT_NAME = '{category_name}'
                                    AND CAT_DESC = '{category_desc}'
                                    AND CAT_STS = '{category_sts}'
                                    AND CAT_ID != {category_id};
                                    """
        c.execute(check_category_exists_sql)
        existing_category = c.fetchone()

        if existing_category:
            #PROMPT
            print("Category with updated values already exists in another row.")
            return

        if category_name == existing_data[0] and category_desc == existing_data[1] and category_sts == existing_data[2]:
            #PROMPT
            print("No changes made to the category details.")
            return

        update_category_data_sql = f""" 
                                        UPDATE categories 
                                        SET CAT_NAME = '{category_name}', CAT_DESC = '{category_desc}', CAT_STS = '{category_sts}'
                                        WHERE CAT_ID = {category_id};
                                    """

        try:
            c = conn.cursor()
            c.execute(update_category_data_sql)
            conn.commit()

            self.ui.product_name_category.setText("")
            self.ui.category_description.setText("")
            self.ui.status_category.setCurrentIndex(0)

            category_names = DBQueries.getCategoryNames(dbFolder)
            self.ui.cat_name_pricelist.clear()
            self.ui.cat_name_pricelist.addItems(category_names)

            DBQueries.displayCategories(self, DBQueries.getAllCategories(dbFolder))

        except Error as e:
            print(e)


    def deleteCategory(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        selected_rows = self.ui.category_table.selectionModel().selectedRows()
        if not selected_rows:
            print("No category selected.")
            return

        if len(selected_rows) == 1:
            category_id = int(self.ui.category_table.item(selected_rows[0].row(), 0).text())

            delete_category_sql = f"""
                                    DELETE FROM categories
                                    WHERE CAT_ID = {category_id};
                                """

            try:
                c = conn.cursor()
                c.execute(delete_category_sql)
                conn.commit()

                category_names = DBQueries.getCategoryNames(dbFolder)
                self.ui.cat_name_pricelist.clear()
                self.ui.cat_name_pricelist.addItems(category_names)

                DBQueries.displayCategories(self, DBQueries.getAllCategories(dbFolder))

            except Error as e:
                print(e)

        else:
            response = input("You have selected multiple categories. Are you sure you want to delete them? (y/n): ").strip().lower()

            if response == 'y':
                category_ids = [int(self.ui.category_table.item(row.row(), 0).text()) for row in selected_rows]

                delete_selected_categories_sql = f"""
                                                DELETE FROM categories
                                                WHERE CAT_ID IN ({', '.join(str(id) for id in category_ids)});
                                            """

                try:
                    c = conn.cursor()
                    c.execute(delete_selected_categories_sql)
                    conn.commit()

                    category_names = DBQueries.getCategoryNames(dbFolder)
                    self.ui.cat_name_pricelist.clear()
                    self.ui.cat_name_pricelist.addItems(category_names)

                    DBQueries.displayCategories(self, DBQueries.getAllCategories(dbFolder))

                except Error as e:
                    print(e)

    def on_category_selection_changed(self):
        selected_rows = self.ui.category_table.selectionModel().selectedRows()
        add_category_btn = self.ui.add_category_btn
        edit_category_btn = self.ui.edit_category_btn
        
        if len(selected_rows) > 0:
            add_category_btn.setEnabled(False)
        else:
            add_category_btn.setEnabled(True)
        
        if len(selected_rows) > 1:
            edit_category_btn.setEnabled(False)
        else:
            edit_category_btn.setEnabled(True)

    #======================= PRICE LIST QUERIES =========================#
    def getCategoryNames(dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        get_category_names_sql = """SELECT CAT_NAME
                                    FROM categories;"""

        try:
            c = conn.cursor()
            c.execute(get_category_names_sql)
            category_names = [row[0] for row in c.fetchall()]

            print(category_names)
            return category_names
        except Error as e:
            print(e)
            return []
    
    def getAllPrices(dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        get_all_prices = '''
                            SELECT p.PROD_ID, c.CAT_NAME, p.PROD_SZ, p.PROD_PRICE
                            FROM product p
                            JOIN categories c ON p.CAT_ID = c.CAT_ID
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

            self.ui.pricelist_table.setRowCount(rowPosition+1)
            prices_tablewidgetitem = QTableWidgetItem()
            self.ui.pricelist_table.setVerticalHeaderItem(rowPosition, prices_tablewidgetitem)

            for item in row:
                self.prices_tablewidgetitem = QTableWidgetItem()
                self.ui.pricelist_table.setItem(rowPosition, itemCount, self.prices_tablewidgetitem)
                self.prices_tablewidgetitem = self.ui.pricelist_table.item(rowPosition, itemCount)
                self.prices_tablewidgetitem.setText(str(item))

                itemCount = itemCount+1
            rowPosition = rowPosition+1
    
    def addPrice(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        product_category = self.ui.cat_name_pricelist.currentText()
        product_size = self.ui.size_pricelist.text()
        product_price = self.ui.price_pricelist.text()

        if not product_size or not product_price:
            #PROMPT
            print("Missing fields.")
            return
        
        check_category_exists_sql = f"""
            SELECT CAT_ID FROM categories WHERE CAT_NAME = '{product_category}';
        """

        c = conn.cursor()
        c.execute(check_category_exists_sql)
        cat_id_result = c.fetchone()

        if not cat_id_result:
            #PROMPT
            print("Category does not exist.")
            return

        cat_id = cat_id_result[0]

        check_price_exists_sql = f"""
                                    SELECT PROD_ID FROM product
                                    WHERE CAT_ID = '{cat_id}'
                                    AND PROD_SZ = '{product_size}'
                                    AND PROD_PRICE = '{product_price}';
                                    """
        c = conn.cursor()
        c.execute(check_price_exists_sql)
        existing_price = c.fetchone()

        if existing_price:
            #PROMPT
            print("Price for product already exists.")
            return


        insert_price_data_sql = f""" 
                                        INSERT INTO product (CAT_ID, PROD_SZ, PROD_PRICE) VALUES ('{cat_id}','{product_size}', '{product_price}'); 
                                    """

        try:
            c = conn.cursor()
            c.execute(insert_price_data_sql)
            conn.commit()

            self.ui.cat_name_pricelist.itemText(0)
            self.ui.size_pricelist.setText("")
            self.ui.price_pricelist.setText("")

            DBQueries.displayPrices(self, DBQueries.getAllPrices(dbFolder))

        except Error as e:
            print(e)
    
    def deletePrice(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        selected_rows = self.ui.pricelist_table.selectionModel().selectedRows()
        if not selected_rows:
            print("No price for product selected.")
            return

        if len(selected_rows) == 1:
            prod_id = int(self.ui.pricelist_table.item(selected_rows[0].row(), 0).text())

            delete_price_sql = f"""
                                    DELETE FROM product
                                    WHERE PROD_ID = {prod_id};
                                """

            try:
                c = conn.cursor()
                c.execute(delete_price_sql)
                conn.commit()

                DBQueries.displayPrices(self, DBQueries.getAllPrices(dbFolder))

            except Error as e:
                print(e)

        else:
            response = input("You have selected multiple prices. Are you sure you want to delete them? (y/n): ").strip().lower()

            if response == 'y':
                prices_ids = [int(self.ui.pricelist_table.item(row.row(), 0).text()) for row in selected_rows]

                delete_selected_prices_sql = f"""
                                                DELETE FROM product
                                                WHERE PROD_ID IN ({', '.join(str(id) for id in prices_ids)});
                                            """

                try:
                    c = conn.cursor()
                    c.execute(delete_selected_prices_sql)
                    conn.commit()

                    DBQueries.displayPrices(self, DBQueries.getAllPrices(dbFolder))

                except Error as e:
                    print(e)