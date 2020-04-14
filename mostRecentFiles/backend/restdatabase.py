#!/usr/bin/env python

#-----------------------------------------------------------------------
# restdatabase.py
# Author: Sunita Srivatsan and Noa Zarur
#-----------------------------------------------------------------------

from sqlite3 import connect
from sys import stderr
from os import path
from menuResult import MenuResult
from orderResult import OrderResult

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
            results.append(result)
            row = cursor.fetchone()
        cursor.close()

        return results
    
    def menuSearchUser(self, restName):
        cursor = self._connection.cursor() 
        restIdString = 'SELECT restaurant_id FROM restaurants ' +\
         'WHERE restaurant_name LIKE "Chennai Chimney"'
        cursor.execute(restIdString)
        restId = cursor.fetchone()[0]
        print("HELLO")
        stmStr = 'SELECT menu.food, menu.description, menu.unit_price, menu.food_id, new_price FROM menu, order_table ' +\
        'WHERE menu.food_id = order_table.food_id;'
        cursor.execute(stmStr)

        results = []
        row = cursor.fetchone()
        while row is not None:  
            result = OrderResult(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
            results.append(result)
            row = cursor.fetchone()
        cursor.close()

        return results

    def inputDiscount(self, discount, foodid):
        cursor = self._connection.cursor() 
        stmstr2 = 'SELECT unit_price FROM menu ' +\
        'WHERE menu.food_id LIKE ?'
        cursor.execute(stmstr2, foodid)
        price = cursor.fetchone()
        quantity = 1
        newPrice = (1 - float(discount)) * float(price[0])
        stmstr = 'UPDATE order_table SET discount = ?, unit_price = ?, new_price = ?, quantity = ? ' +\
        'WHERE food_id LIKE ?;'
        
        # stmstr = 'INSERT INTO order_table (discount, unit_price, new_price, quantity, food_id) VALUES (?, ?, ?, ?, ?);'

        # 'WHERE food_id LIKE ?

        print(str(foodid) + " " + str(discount))
        #stmstr = 'INSERT INTO order.discount VALUES ?'  +\
        #'WHERE food_id LIKE ?'
        arguments = (discount, price[0], newPrice, quantity, foodid)
        cursor.execute(stmstr, arguments) 
        # teststmstr = 'SELECT order.discount FROM order'  +\
        # 'WHERE food_id LIKE ?'
        # cursor.execute(teststmstr, food_id)
        # print(cursor.fetchone())
        cursor.close()
        return 

    def pullNewPrice(self, food_id):
        cursor = self._connection.cursor() 
        stmstr = 'SELECT new_price FROM order_table, menu ' +\
        'WHERE menu.food_id LIKE ?;'
        cursor.execute(stmstr, food_id)
        newPrice = cursor.fetchone()
        cursor.close()
        print(newPrice[0])
        print("hello")
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
