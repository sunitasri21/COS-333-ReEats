#!/usr/bin/env python

#-----------------------------------------------------------------------
# result.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

class MenuResult:

    def __init__(self, food, description, price, food_id):
        self.food = food
        self.description = description
        #self.dietary = dietary
        self.price = price 

    def __str__(self):
        return self.food + ', ' + self.description
        + ',' + self.price 

    def getFood(self):
        return self.food

    def getDescription(self):
        return self.description

    # def getDietary(self):
    #     return self.dietary

    def getPrice(self):
        return self.price

    def getId(self):
        return self.food_id

