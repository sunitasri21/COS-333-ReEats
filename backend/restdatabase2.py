#!/usr/bin/env python

#-----------------------------------------------------------------------
# restdatabase.py
# Author: Sunita Srivatsan and Noa Zarur
#-----------------------------------------------------------------------

from sqlite3 import connect
from sys import stderr
from os import path
from orderResult2 import OrderResult
import psycopg2
import time 
import datetime
from datetime import date

# from menuResult import MenuResults

#-----------------------------------------------------------------------
heroku = True

class Database:
    def __init__(self):
        self._connection = None

    def connect(self):  
        if heroku:    
            DATABASE_URL = 'postgres://nkprqcoopdaeyb:4c1332d24e848ae3d5e9554120db7b65e2fe58c0913f19fbed082dd106d7c979@ec2-34-195-169-25.compute-1.amazonaws.com:5432/d9dpro4r60j6ub'
            self._connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:
            conn_string = "host='localhost' dbname='reeats10'"
            self._connection = psycopg2.connect(conn_string)   

        # if not path.isfile(DATABASE_NAME):
        #     raise Exception("database reeats.db not found")
        # self._connection = connect(DATABASE_NAME)
        # self._connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        # self._connection = psycopg2.connect(conn_string)   

    def disconnect(self):
        self._connection.close()

    def account_login(self, username, password):
        cursor = self._connection.cursor() 
        cursor.execute("SELECT * FROM _restaurant_accounts WHERE username = %s AND password = %s", (username, password, )); 
        rest = cursor.fetchone()
        cursor.execute("SELECT * FROM _user_account WHERE username = %s AND password = %s", (username, password, )); 
        user = cursor.fetchone()
        cursor.close()
        return rest, user
    
    # Searches for an username in the accounts table 
    def account_search(self, username, password):
        cursor = self._connection.cursor() 
        cursor.execute("SELECT * FROM _restaurant_accounts WHERE username = %s AND password = %s", (username, password, )); 
        rest = cursor.fetchone()
        cursor.execute("SELECT * FROM _user_account WHERE username = %s AND password = %s", (username, password, )); 
        user = cursor.fetchone()
        cursor.close()
        return rest, user

    def user_search(self, username):
        cursor = self._connection.cursor() 
        cursor.execute("SELECT * FROM _restaurant_accounts WHERE restaurant_id = %s", (username, )); 
        rest = cursor.fetchone()
        cursor.execute("SELECT * FROM _user_account WHERE user_id = %s", (username, ))
        user = cursor.fetchone()
        cursor.close()
        return rest, user

    def restaurant_search(self, restaurant_id):
        cursor = self._connection.cursor() 
        cursor.execute("SELECT restaurant_name FROM _restaurants WHERE restaurant_id = %s", (restaurant_id, ))
        restaurant_name = cursor.fetchone()[0]
        cursor.close()
        return restaurant_name

    def pullOrderId(self, user_id):
        cursor = self._connection.cursor() 
        user_id = int(user_id)
        cursor.execute("SELECT order_id FROM _order_join WHERE user_id = %s", (user_id, ))
        orderId = cursor.fetchone()
        cursor.close()
        return orderId[0]

    def pullConfirmedOrders(self, user_id, orderid):
        cursor = self._connection.cursor() 
        user_id = int(user_id)
        cursor.execute("SELECT order_id FROM _order_join WHERE user_id = %s", (user_id, )); 
        orderId = cursor.fetchone()
        cursor.close()
        return orderId[0]

    def previewAllDiscounts(self):
        cursor = self._connection.cursor() 
        stmstr = 'SELECT discount, unit_price, new_price, quantity, food FROM _menu;'
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

    def menuSearch(self, restName):
        cursor = self._connection.cursor() 
        rest_name = 'Chennai Chimney'
        cursor.execute("SELECT restaurant_id FROM _restaurants WHERE restaurant_name = %s", (rest_name, ))
        restId = cursor.fetchone()[0]
        menu_id = '1'
        cursor.execute("SELECT food, description, unit_price, food_id FROM _menu WHERE restaurant_id = %s ORDER BY food_id ASC", (menu_id, ))
        print("inDatabaseSearch")
        results = []
        row = cursor.fetchone()
        while row is not None:  
            result = OrderResult(food=str(row[0]), description=str(row[1]), unit_price=str(row[2]), food_id=str(row[3]))
            results.append(result)
            print('id', result.getId())
            row = cursor.fetchone()
        cursor.close()

        return results

    def menuSearchUser(self, restName):
        cursor = self._connection.cursor() 
        rest_name = 'Chennai Chimney'
        cursor.execute("SELECT restaurant_id FROM _restaurants WHERE restaurant_name = %s", (rest_name, ))
        restId = cursor.fetchone()[0]
        # 'WHERE menu.food_id = order_table.food_id;'
        cursor.execute("SELECT food, description, unit_price, food_id, discount, new_price, quantity FROM _menu WHERE NOW() - starttime > INTERVAL '1 minute' ")

        results = []
        row = cursor.fetchone()
        while row is not None:  
            discount = row[4]
            # print("d: " + str(discount))
            quantity = row[6]
            # print("q: " + str(quantity))
            if (discount is not None and discount != '') and (quantity != '' and quantity != '0'):
                result = OrderResult(food=str(row[0]), description=str(row[1]), unit_price=str(row[2]), food_id=str(row[3]), new_price=str(row[5]), quantity=quantity)
                results.append(result)
            row = cursor.fetchone()
        cursor.close()

        return results

    # Adds a new user to the database during Registration
    def add_user(self, user_id, username, password, email):
        cursor = self._connection.cursor() 
        cursor.execute("INSERT INTO _user_account (user_id, username, password, email) VALUES (%s, %s , %s , %s)", (user_id, username, password, email,)); 
        self._connection.commit()
        cursor.close()
        return 

    def inputDiscount(self, discount, quantity, foodid, startTime, endTime):
        cursor = self._connection.cursor() 
        foodid = int(foodid)
        cursor.execute("SELECT food, unit_price FROM _menu WHERE food_id = %s", (foodid, )); 
        discount = float(discount)

        result = cursor.fetchone()
        food = result[0]
        price = result[1]
        quantity = int(quantity)
        if quantity == None:
            quantity = 1
        if discount == None:
            discount = 0.0
        start = str(date.today()) + " " + startTime      
        end = str(date.today()) + " " + endTime        
        
        
        newPrice = (1 - float(discount)) * float(price)
        newPrice = '{:.2f}'.format(newPrice)
        arguments = (discount, newPrice, quantity, foodid) 
        if (discount >= 0 and discount <= 1):
            cursor.execute("UPDATE _menu SET discount = %s, new_price = %s, quantity = %s, \
                starttime = TO_TIMESTAMP( %s, 'YYYY-MM-DD HH24:mi') , endtime = TO_TIMESTAMP(%s,'YYYY-MM-DD HH24:mi') WHERE food_id= %s", \
                 (discount, newPrice, quantity, start, end, foodid,)); 
        self._connection.commit()
        cursor.close()
        return 

    def updateQuantity(self, quantity, foodid):
        cursor = self._connection.cursor() 
        foodid = int(foodid)
        cursor.execute("SELECT quantity FROM _menu WHERE food_id = %s", (foodid, )); 
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

        newQuant = int(originalQuantity) - int(quantity)   

        arguments = (newQuant, foodid) 
        if (int(originalQuantity) >= int(quantity)):
            cursor.execute("UPDATE _menu SET quantity = %s WHERE food_id = %s", (newQuant, foodid, ));  
        self._connection.commit()
        cursor.close()
        return 

    def pullNewPrice(self, food_id):
        cursor = self._connection.cursor() 
        food_id = int(food_id)
        cursor.execute("SELECT new_price FROM _menu WHERE food_id = %s", (food_id, )) 
        newPrice = cursor.fetchone()
        cursor.close()
        return newPrice[0]

    def pullName(self, food_id):
        cursor = self._connection.cursor()
        food_id = int(food_id)
        cursor.execute("SELECT food FROM _menu WHERE food_id = %s", (food_id, ))
        newPrice = cursor.fetchone()
        cursor.close()
        return newPrice[0]

    def inputOrderId(self, userid, price, quantity, foodid, food, orderid, confirmed):
        cursor = self._connection.cursor() 
        userid = int(userid)
        foodid = int(foodid)
        price = float(price)
        orderid = orderid
        quantity = int(quantity)
        qrCode = ''
        paid = 0 

        arguments = (price, quantity, food, foodid, orderid, confirmed, userid)

        cursor.execute("INSERT INTO _order_table (new_price, quantity, food, food_id, order_id, confirmed, user_id, paid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
            ON CONFLICT (user_id, order_id, food_id) DO UPDATE \
            SET new_price = %s, quantity = %s, food = %s, food_id = %s, order_id = %s, confirmed = %s, user_id = %s, paid = %s",
            (price, quantity, food, foodid, orderid, confirmed, userid, paid, price, quantity, food, foodid, orderid, confirmed, userid, paid, )); 

        arguments2 = (orderid, qrCode, userid) 
        cursor.execute("UPDATE _order_join SET order_id = %s, qrCode = %s, user_id = %s", (orderid, qrCode, userid, )); 

        self._connection.commit()
        cursor.close()
        return 

# <<<<<<< HEAD
#         # we had issues with replace so might be insert for stmstr
#         stmstr = 'UPDATE order_table SET new_price=?,  quantity=?, food=?, food_id=?, order_id=?, confirmed=?, user_id=? ' +\
#         'WHERE order_table.food_id LIKE ?;'
# =======
# >>>>>>> 315fa5d5e2f03d435cee8f05c5079b00a8dfb913
        # arguments = (price, quantity, food, foodid, orderid, confirmed, userid)
        # cursor.execute("INSERT INTO _order_table (new_price, quantity, food, food_id, order_id, confirmed, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
        #     (price, quantity, food, foodid, orderid, confirmed, userid, )); 

    def confirmedOrder(self, userid, orderid, confirmed):
        cursor = self._connection.cursor() 
        userid = int(userid)
        confirmed = int(confirmed)
        paid = 0 

        arguments3 = (userid, orderid, confirmed)
        cursor.execute("SELECT food_id, food, new_price, quantity FROM _order_table WHERE user_id = %s AND order_id = %s AND confirmed = %s AND paid = %s", (userid, orderid, confirmed, paid, )); 
        results = []
        total_value = 0.0
        row = cursor.fetchone()
        while row is not None: 
            # print(row)
            result = OrderResult(food_id = str(row[0]), food = str(row[1]), new_price = str(row[2]), quantity = str(row[3]))
            results.append(result)
            total_value = float(total_value) + float(row[3]) * float(row[2])
            row = cursor.fetchone()
        cursor.close()
        return results, total_value

    def updateExpiredDiscounts(self):
        cursor = self._connection.cursor() 
        zero_quantity = 0
        command = "UPDATE _menu SET quantity = %s WHERE NOW() - endtime > INTERVAL '1 minute'"
        cursor.execute(command, (zero_quantity,));
        self._connection.commit()
        cursor.close()
        return 
    
    
    def inputPaidOrder(self, userid, orderid):
        cursor = self._connection.cursor() 
        userid = int(userid)
        paid = 1
        confirmed = 1

        arguments3 = (userid, orderid)
        cursor.execute("SELECT food_id, food, new_price, quantity FROM _order_table WHERE user_id = %s AND order_id = %s", (userid, orderid, )); 
        results = []
        row = cursor.fetchone()
        while row is not None: 
            # print(row)
            result = OrderResult(food_id = str(row[0]), food = str(row[1]), new_price = str(row[2]), quantity = str(row[3]))
            results.append(result)
            row = cursor.fetchone()

        for result in results:
            foodid = result.getId()
            food = result.getFood()
            quantity = result.getQuantity()
            price = result.getNewPrice()
            cursor.execute("INSERT INTO _order_table (new_price, quantity, food, food_id, order_id, confirmed, user_id, paid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
            ON CONFLICT (user_id, order_id, food_id) DO UPDATE \
            SET new_price = %s, quantity = %s, food = %s, food_id = %s, order_id = %s, confirmed = %s, user_id = %s, paid = %s",
            (price, quantity, food, foodid, orderid, confirmed, userid, paid, price, quantity, food, foodid, orderid, confirmed, userid, paid, )); 

        self._connection.commit()
        cursor.close()
        return 

    def paidOrder(self, userid):
        cursor = self._connection.cursor() 
        userid = int(userid)
        paid = 1

        arguments3 = (userid, confirmed)
        cursor.execute("SELECT food_id, food, new_price, quantity FROM _order_table WHERE user_id = %s AND paid = %s", (userid, paid, )); 
        results = []
        total_value = 0.0
        row = cursor.fetchone()
        while row is not None: 
            # print(row)
            result = OrderResult(food_id = str(row[0]), food = str(row[1]), new_price = str(row[2]), quantity = str(row[3]))
            results.append(result)
            total_value = float(total_value) + float(row[3]) * float(row[2])
            row = cursor.fetchone()
        cursor.close()
        return results, total_value

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
