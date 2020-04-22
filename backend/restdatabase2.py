#!/usr/bin/env python

#-----------------------------------------------------------------------
# restdatabase.py
# Author: Sunita Srivatsan and Noa Zarur
#-----------------------------------------------------------------------

from sqlite3 import connect
from sys import stderr
from os import path
from orderResult2 import OrderResult

# from menuResult import MenuResult

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
    
    def account_login(self, username, password):
        cursor = self._connection.cursor() 
        rest_string = 'SELECT * FROM restaurant_accounts WHERE username LIKE ? AND password LIKE ?;'
        user_string = 'SELECT * FROM user_accounts WHERE username LIKE ? AND password LIKE ?;'
        cursor.execute(rest_string, (username, password,))
        rest = cursor.fetchone()
        cursor.execute(user_string, (username, password,))
        user = cursor.fetchone()
        cursor.close()
        return rest, user
    
    # Searches for an username in the accounts table 
    def account_search(self, username):
        cursor = self._connection.cursor() 
        rest_string = 'SELECT * FROM restaurant_accounts WHERE username LIKE ?;'
        user_string = 'SELECT * FROM user_accounts WHERE username LIKE ?;'
        cursor.execute(rest_string, (username,))
        rest = cursor.fetchone()
        cursor.execute(user_string, (username,))
        user = cursor.fetchone()
        cursor.close()
        return rest, user
    
    # Adds a new user to the database during Registration
    def add_user(self, username, password, email):
        cursor = self._connection.cursor() 
        add_string = 'INSERT INTO user_accounts VALUES ( ? , ? , ? );'
        cursor.execute(add_string, (username, password, email,))
        self._connection.commit()
        cursor.close()
        return
    
    def restaurant_search(self, restaurant_id):
        cursor = self._connection.cursor() 
        restString = 'SELECT restaurant_name FROM restaurants ' +\
         'WHERE restaurant_id = ?'
        cursor.execute(restString, (restaurant_id,))
        restaurant_name = cursor.fetchone()[0]
        cursor.close()
        return restaurant_name

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
            result = OrderResult(food=str(row[0]), description=str(row[1]), unit_price=str(row[2]), food_id=str(row[3]))
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
        stmStr = 'SELECT food, description, unit_price, food_id, discount, new_price, quantity FROM menu'
        # 'WHERE menu.food_id = order_table.food_id;'
        cursor.execute(stmStr)

        results = []
        row = cursor.fetchone()
        while row is not None:  
            discount = row[4]
            quantity = row[6]
            if discount is not None and quantity != 0:
                result = OrderResult(food=str(row[0]), description=str(row[1]), unit_price=str(row[2]), food_id=str(row[3]), new_price=str(row[5]), quantity=quantity)
                results.append(result)
            row = cursor.fetchone()
        cursor.close()

        return results

    def inputDiscount(self, discount, quantity, foodid):
        cursor = self._connection.cursor() 
        stmstr2 = 'SELECT food, unit_price FROM menu ' +\
        'WHERE menu.food_id LIKE ?'
        foodid = int(foodid)
        cursor.execute(stmstr2, (foodid, ))
        discount = float(discount)

        result = cursor.fetchone()
        food = result[0]
        price = result[1]
        quantity = int(quantity)
        if quantity == None:
            quantity = 1
        if discount == None:
            discount = 0.0
        print(quantity)
        newPrice = (1 - float(discount)) * float(price)
        newPrice = '{:.2f}'.format(newPrice)
        stmstr = 'UPDATE menu SET discount = ?, new_price = ?, quantity = ? ' +\
        'WHERE menu.food_id LIKE ?;'
        arguments = (discount, newPrice, quantity, foodid) 
        if (discount >= 0 and discount <= 1):
            cursor.execute(stmstr, arguments) 
        self._connection.commit()
        cursor.close()
        return 

    def updateQuantity(self, quantity, foodid):
        cursor = self._connection.cursor() 
        stmstr2 = 'SELECT quantity FROM menu ' +\
        'WHERE menu.food_id LIKE ?'
        foodid = int(foodid)
        cursor.execute(stmstr2, (foodid, ))
        result = cursor.fetchone()
        originalQuantity = result[0]

        # result = cursor.fetchone()
        # food = result[0]
        # price = result[1]
        # quantity = int(quantity)
        # if quantity == None:
        #     quantity = 1
        # if discount == None:
        #     discount = 0.0
        # print(quantity)
        # newPrice = (1 - float(discount)) * float(price)
        # newPrice = '{:.2f}'.format(newPrice)
        stmstr = 'UPDATE menu SET quantity = ? ' +\
        'WHERE menu.food_id LIKE ?;'

        newQuant = int(originalQuantity) - int(quantity)   

        arguments = (newQuant, foodid) 
        if (originalQuantity >= int(quantity)):
            cursor.execute(stmstr, arguments) 
        self._connection.commit()
        cursor.close()
        return 


    def pullNewPrice(self, food_id):
        cursor = self._connection.cursor() 
        stmstr = 'SELECT new_price FROM menu ' +\
        'WHERE menu.food_id LIKE ?;'
        food_id = int(food_id)
        cursor.execute(stmstr, (food_id, )) 
        newPrice = cursor.fetchone()
        cursor.close()
        return newPrice[0]

    def pullName(self, food_id):
        cursor = self._connection.cursor() 
        stmstr = 'SELECT food FROM menu ' +\
        'WHERE menu.food_id LIKE ?;'
        food_id = int(food_id)
        cursor.execute(stmstr, (food_id, ))
        newPrice = cursor.fetchone()
        cursor.close()
        return newPrice[0]

    def previewAllDiscounts(self):
        cursor = self._connection.cursor() 
        stmstr = 'SELECT discount, unit_price, new_price, quantity, food FROM menu;'
        cursor.execute(stmstr)
        results = []
        row = cursor.fetchone()
        while row is not None: 
            discount = row[0]
            if discount is not None:
                result = OrderResult(discount=str(row[0]), unit_price=str(row[1]), new_price=str(row[2]), quantity=str(row[3]), food=str(row[4]))
                results.append(result)
            row = cursor.fetchone()
        cursor.close()
        return results

    def inputOrderId(self, user_id, food, food_id, order_id, quantity, newPrice):
        cursor = self._connection.cursor() 
        # user_id = int(user_id)
        quantity = int(quantity)
        newPrice = float(newPrice)
        food_id = int(food_id)
        stmstr = 'UPDATE order_table SET new_price = ?, order_id = ?, quantity = ?, food = ? '+\
        'WHERE food_id = ?;'
        arguments = (newPrice, order_id, quantity, food, food_id)
        cursor.execute(stmstr, arguments)
        # stmstr2 = 'REPLACE INTO order_join (user_id, order_id) VALUES (?, ?);'
        # arguments2 = (user_id, order_id)
        # cursor.execute(stmstr2, arguments2)
        self._connection.commit()

        cursor.close()





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
