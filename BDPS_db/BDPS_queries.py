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

        insert_category_data_sql = f""" INSERT INTO categories (CAT_NAME, CAT_DESC, CAT_STS) VALUES ('{category_name}','{category_desc}', '{category_sts}'); """

        if not conn.cursor().execute(insert_category_data_sql):
            print("Could not insert")
        else:
            conn.commit()

            self.ui.product_name_category.setText("")
            self.ui.category_description.setText("")
            self.ui.status_category.itemText(-1)

            DBQueries.displayCategories(self, DBQueries.getAllCategories(dbFolder))

    def displayCategories(self, rows):
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