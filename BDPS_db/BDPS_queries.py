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
    
    def addCategory(self, dbFolder):
        conn = DBQueries.create_connection(dbFolder)

        category_name = self.ui.product_name_category.text()
        category_desc = self.ui.category_description.toPlainText()
        category_sts = self.ui.status_category.currentText()
        
        if not category_name or not category_desc:
            #PROMPT
            print("Missing fields.")
            return

        insert_category_data_sql = f""" 
                                        INSERT INTO categories (CAT_NAME, CAT_DESC, CAT_STS) VALUES ('{category_name}','{category_desc}', '{category_sts}'); 
                                    """

        if not conn.cursor().execute(insert_category_data_sql):
            #PROMPT
            print("Could not insert")
        else:
            conn.commit()

            self.ui.product_name_category.setText("")
            self.ui.category_description.setText("")
            self.ui.status_category.itemText(0)

            DBQueries.displayCategories(self, DBQueries.getAllCategories(dbFolder))

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

                    DBQueries.displayCategories(self, DBQueries.getAllCategories(dbFolder))

                except Error as e:
                    print(e)

    def on_category_selection_changed(self):
        selected_row = self.ui.category_table.currentRow()
        add_category_btn = self.ui.add_category_btn

        if selected_row >= 0:
            add_category_btn.setEnabled(False)
        else:
            add_category_btn.setEnabled(True)

    def on_selection_changed(self):
        selected_rows = self.ui.category_table.selectionModel().selectedRows()
        edit_category_btn = self.ui.edit_category_btn

        if len(selected_rows) > 1:
            edit_category_btn.setEnabled(False)
        else:
            edit_category_btn.setEnabled(True)

    #======================= PRICE LIST QUERIES =========================#
