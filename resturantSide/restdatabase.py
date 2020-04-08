#!/usr/bin/env python

#-----------------------------------------------------------------------
# restdatabase.py
# Author: Sunita Srivatsan and Noa Zarur
#-----------------------------------------------------------------------

from sqlite3 import connect
from sys import stderr
from os import path
from menuResult import MenuResult

#-----------------------------------------------------------------------

class Database:
    def __init__(self):
        self._connection = None

    def connect(self):      
        DATABASE_NAME = 'reeats.db'
        if not path.isfile(DATABASE_NAME):
            raise Exception("database reeats.db not found")
        self._connection = connect(DATABASE_NAME)
                    
    def disconnect(self):
        self._connection.close()

    def menuSearch(self, restName):
        cursor = self._connection.cursor() 
        restIdString = 'SELECT restaurant_id FROM restaurants ' +\
         'WHERE restaurant_name LIKE "Chennai Chimney"'
        cursor.execute(restIdString)
        restId = cursor.fetchone()[0]
        stmStr = 'SELECT food, description, unit_price, food_id FROM menu ' +\
        'WHERE menu.restaurant_id = 1;'
        cursor.execute(stmStr)

        results = []
        row = cursor.fetchone()
        while row is not None:  
            result = MenuResult(str(row[0]), str(row[1]), str(row[2]), str(row[3]))
            results.append(result);
            row = cursor.fetchone()
        cursor.close()

        return results

    def inputDiscount(self, discount, food_id):
        cursor = self._connection.cursor() 
        stmstr2 = 'SELECT unit_price FROM menu ' +\
        'WHERE menu.food_id LIKE ?'
        cursor.execute(stmstr2, food_id)
        price = cursor.fetchone()
        quantity = 1
        newPrice = (1 - float(discount)) * float(price)
        stmstr = 'INSERT INTO order (food_id, discount, unit_price, newPrice, quantity) VALUES ?;'
        #stmstr = 'INSERT INTO order.discount VALUES ?'  +\
        #'WHERE food_id LIKE ?'
        arguments = [food_id, discount, price, newPrice, quantity]
        cursor.execute(stmstr, arguments) 
        # teststmstr = 'SELECT order.discount FROM order'  +\
        # 'WHERE food_id LIKE ?'
        # cursor.execute(teststmstr, food_id)
        # print(cursor.fetchone())
        cursor.close()
        return 

    def pullNewPrice(self, food_id):
        cursor = self._connection.cursor() 
        stmstr = 'SELECT newPrice FROM order ' +\
        'WHERE menu.food_id LIKE ?'
        cursor.execute(stmstr, food_id)
        newPrice = cursor.fetchone()
        cursor.close()
        return newPrice[0]


#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    database.connect()
    results = database.menuSearch("Chennai Chimney")
    for result in results:
        print('result', result)
    # print(results2.getCourseId())
    # print(results2.getArea())
    # print(results2.getDeptandNumber())
    # print(results2.getTitle())
    # print(results2.getDescription())
    # print(results2.getPrereqs())
    # print(results2.getProfs())
    # print(results2.getDays())
    # print(results2.getStarttime())
    # print(results2.getEndtime())
    # print(results2.getBuilding())
    # print(results2.getRoom())
    database.disconnect()
