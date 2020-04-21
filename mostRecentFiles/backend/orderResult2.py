#!/usr/bin/env python

#-----------------------------------------------------------------------
# OrderResult.py
# Author: Arjun Sai Krishnan and Sunita Srivatsan 
#-----------------------------------------------------------------------

class OrderResult:

    def __init__(self, food_id=1, discount='', unit_price=1, new_price=1, quantity=1, food='', description='', order_id=''):
        self.food = food
        self.food_id = food_id 
        self.discount = discount
        #self.dietary = dietary
        self.unit_price = unit_price
        self.new_price = new_price 
        self.quantity = quantity 
        self.description = description
        self.order_id = order_id

    def __str__(self):
        return self.food 
        + ',' + self.price 

    def getFood(self):
        return self.food

    def getId(self):
        return self.food_id
    
    def getPrice(self):
        return self.unit_price
    
    def getNewPrice(self):
        return self.new_price

    def getDescription(self):
        return self.description

    def getQuantity(self):
        return self.quantity


    def getDiscount(self):
        return self.discount

    def getOrderId(self):
        return self.order_id

