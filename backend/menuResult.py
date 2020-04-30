#!/usr/bin/env python

#-----------------------------------------------------------------------
# MenuResult.py
# Author: Arjun Krishnan
#-----------------------------------------------------------------------

class MenuResult:

    def __init__(self, food, description, price, food_id):
        self.food = food
        self.description = description
        #self.dietary = dietary
        self.price = price
        self.food_id = food_id 
        # self.discount = discount 

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

    # def getDiscount(self):
    #     return self.discount

