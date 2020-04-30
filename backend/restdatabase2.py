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

# from menuResult import MenuResults

#-----------------------------------------------------------------------

class Database:
    def __init__(self):
        self._connection = None

    def connect(self):      
        DATABASE_URL = 'postgres://cavaxcayvoqxdp:d738fe5b698af40d07276a90ec25bdbb24eb4b89bb984fa6af075828c3df7d5b@ec2-54-165-36-134.compute-1.amazonaws.com:5432/d4pdqjkun0inr5'
        conn_string = "host='localhost' dbname='reeats6' user='arjunsaikrishnan' password='waterside2007'"
        # if not path.isfile(DATABASE_NAME):
        #     raise Exception("database reeats.db not found")
        # self._connection = connect(DATABASE_NAME)
        self._connection = psycopg2.connect(DATABASE_URL, sslmode='require')
                    
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
        rest_name = 'Chennai Chimney'
        cursor.execute("SELECT restaurant_id FROM _restaurants WHERE restaurant_name = %s", (rest_name, ))
        restId = cursor.fetchone()[0]
        # 'WHERE menu.food_id = order_table.food_id;'
        cursor.execute("SELECT food, description, unit_price, food_id, discount, new_price, quantity FROM _menu")

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

    def inputDiscount(self, discount, quantity, foodid):
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
        print(quantity)
        newPrice = (1 - float(discount)) * float(price)
        newPrice = '{:.2f}'.format(newPrice)
        arguments = (discount, newPrice, quantity, foodid) 
        if (discount >= 0 and discount <= 1):
            cursor.execute("UPDATE _menu SET discount = %s, new_price = %s, quantity = %s WHERE food_id= %s", (discount, newPrice, quantity, foodid, )); 
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

        arguments = (price, quantity, food, foodid, orderid, confirmed, userid)
        cursor.execute("INSERT INTO _order_table (new_price, quantity, food, food_id, order_id, confirmed, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
            (price, quantity, food, foodid, orderid, confirmed, userid, )); 

        arguments2 = (orderid, qrCode, userid) 
        cursor.execute("UPDATE _order_join SET order_id = %s, qrCode = %s, user_id = %s", (orderid, qrCode, userid, )); 

        self._connection.commit()
        cursor.close()
        return 

    def confirmedOrder(self, userid, orderid, confirmed):
        cursor = self._connection.cursor() 
        userid = int(userid)
        confirmed = int(confirmed)

        arguments3 = (userid, orderid, confirmed)
        cursor.execute("SELECT food, new_price, quantity FROM _order_table WHERE user_id = %s AND order_id = %s AND confirmed = %s", (userid, orderid, confirmed, )); 
        results = []
        total_value = 0.0
        row = cursor.fetchone()
        while row is not None: 
            # print(row)
            result = OrderResult(food = str(row[0]), new_price = str(row[1]), quantity = str(row[2]))
            results.append(result)
            total_value = float(total_value) + float(row[2]) * float(row[1])
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