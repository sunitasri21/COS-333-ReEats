#!/usr/bin/env python

#-----------------------------------------------------------------------
# completeOrder.py
# Author: Arjun Sai Krishnan and Sunita Srivatsan 
#-----------------------------------------------------------------------

class completeOrder:

    def __init__(self, order_id=1, qrCode='', user_id=1):
        self.order_id = order_id
        self.qrCode = qrCode
        self.user_id = user_id

    def __str__(self):
        return self.food 
        + ',' + self.price 

    def getOrderId(self):
        return self.order_id

    def getQrCode(self):
        return self.qrCode
    
    def getUserId(self):
        return self.user_id
    
