import os
import sys
import sqlite3
from sqlite3 import Error
from PyQt5.QtWidgets import QTableWidgetItem


class DBQueries:
    
    def __init__(self, arg):
        super(DBQueries, self).__init__()
        self.arg = arg

    def dbconnect(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        
        return conn

    def main(dbFolder):
        conn = DBQueries.dbconnect(dbFolder)

    #========================= CATEGORIES =============================#
    def getCategories(dbFolder):
        conn = DBQueries.dbconnect(dbFolder)

        getCategories = "SELECT * FROM categories;"
        try:
            c = conn.cursor()
            c.execute(getCategories)
            return c
        except Error as e:
            print(e)
    
    def addCategories(self, dbFolder):
        conn = DBQueries.dbconnect(dbFolder)

        category_name = self.ui.product_name_category.text()
        category_desc = self.ui.category_description.text()
        category_sts = self.ui.status_category.text()

        insert_category_data = "INSERT INTO categories(CAT_NAME, CAT_DESC, CAT_STS) VALUES('{category_name}', '{category_desc}', '{category_sts}');"
        
        if not conn.cursor().execute(insert_category_data):
            print("Unable to add")
        else:
            conn.commit()

            self.ui.product_name_category.setText("")
            self.ui.category_description.setText("")
            self.ui.status_category.setText("")

    """def displayCategories(self, row):

        for row in row:
            #rowPosition = self.ui.category_table.rowCount()

            if rowPosition > row[0]:
                continue
            
            categoryCount = 0

            self.ui.category_table.setRowCount(rowPosition+1)
            categorywidgetitem = QTableWidgetItem
            self.ui.category_table.setVerticalHeaderItem(rowPosition, categorywidgetitem)
        
        for category in row:
            self.category_widgetitem = QTableWidgetItem()
            self.ui.category_table.setItem(rowPosition, categoryCount, self.category_widgetitem)
            self.category_widgetitem = self.ui.category_table.category(rowPosition, categoryCount)
            self.category_widgetitem.setText(str(category))

            categoryCount = categoryCount+1
        
        #rowPosition = rowPosition+1

    def close_connection(self):
        self.db_conn.close()
    """

