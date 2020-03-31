#!/usr/bin/env python

#-----------------------------------------------------------------------
# regdatabase.py
# Author: Sunita Srivatsan
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
        print(restName)
        restIdString = 'SELECT restaurant_id FROM restaurants ' +\
         'WHERE restaurant_name = ?'
        cursor.execute(restIdString, restName)
        restId = cursor.fetchone()
        print(restId)

        stmStr = 'SELECT food, description, price, vegan, spicy ' + \
            'FROM menu ' +\
            'JOIN dietary ON menu.food_id = dietary.food_id ' +\
            'WHERE menu.restaurant_id = ? ORDER BY price ASC;'
        cursor.execute(stmStr, restId)

        results = []
        row = cursor.fetchone()
        while row is not None:  
            result = MenuResult(str(row[0]), str(row[1]), str(row[2]), (str(row[3]), str(row[4])))
            results.append(result);
            row = cursor.fetchone()
        cursor.close()

        return results

#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    database.connect()
    results = database.menuSearch("chennai")
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
