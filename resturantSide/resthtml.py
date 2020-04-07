#!/usr/bin/env python

#-----------------------------------------------------------------------
# resthtml.py
# Author: Sunita Srivatsan
#-----------------------------------------------------------------------
import flask 
from sys import argv, stderr
from restdatabase import Database
from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
import jinja2
from sys import exit, argv, stderr
import os
from flask import jsonify

#-----------------------------------------------------------------------

template_dir = os.path.join(os.path.dirname(__file__), '.')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

# app = Flask(__name__, template_folder='.')

# variables that are accessible from anywhere
# source: https://stackoverflow.com/questions/14384739/how-can-i-add-a-background-thread-to-flask
# commonDataStruct = {}
# # lock to control access to variable
# dataLock = threading.Lock()
# # thread handler
# yourThread = threading.Thread()


app = Flask(__name__,  template_folder='.')

    # def interrupt():
    #     global yourThread
    #     yourThread.cancel()

    # def doStuff():
    #     global commonDataStruct
    #     global yourThread
    #     with dataLock:
    #     # Do your stuff with commonDataStruct Here

    #     # Set the next thread to happen
    #     yourThread = threading.Timer(POOL_TIME, doStuff, ())
    #     yourThread.start()   

    # def doStuffStart():
    #     # Do initialisation stuff here
    #     global yourThread
    #     # Create your thread
    #     yourThread = threading.Timer(POOL_TIME, doStuff, ())
    #     yourThread.start()

    # Initiate
    # doStuffStart()
    # # When you kill Flask (SIGTERM), clear the trigger for the next thread
    # atexit.register(interrupt)
#     return app

# app = create_app()

# def handleDiscount(discount):
#     #FIGURE OUT HOW TO GET FOOD ID FROM HTML 
#     #food_id = request.args.get('item')
#     inputDiscount(discount, food_id)
#     app.doStuffStart()
#     app.doStuffStart()


@app.route('/', methods=['GET'])
def searchResults():
    restName = str(request.args.get('restName')) or ""
    discount = request.args.get('discount', default=1) 
    # items = {}
    # items['food'] = dept
    # queries['num'] = num
    # queries['area'] = area
    # queries['title'] = title
     
    database = Database()
    try:
        database.connect()
        searchResults = database.menuSearch(restName)
        # if discount != 1:
        #     print('hello')
        #     handleDiscount(discount, request.args.get(item.getFood()))

    except Exception as e:
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)
        # html = render_template('regerror.html', errormessage=errorMsg)
        # response = make_response(html)
        # return response
        exit(1)


    database.disconnect()
    # discountedPrice = []

    # for result in searchResults:
    #     discountedPrice.append(discount * result.getPrice())

    template = jinja_env.get_template("restFirstPage.html")

    html = render_template(template, restaurant=searchResults, discount=discount)
    response = make_response(html)
    return response         

# -----------------------------------------------------------------------

@app.route('/checkoutPage', methods=['GET'])
def checkoutPage():
    html = render_template('checkoutPage.html')
    response = make_response(html)
    return response

# -----------------------------------------------------------------------

@app.route('/accountPage', methods=['GET'])
def accountPage():
    html = render_template('accountPage.html')
    response = make_response(html)
    return response     

# -----------------------------------------------------------------------

@app.route('/feedbackPage', methods=['GET'])
def feedbackPage():
    html = render_template('feedbackPage.html')
    response = make_response(html)
    return response    

# -----------------------------------------------------------------------

# @app.route('api/updateDiscount', methods=['post'])
# def updateDiscount():
#     item_num = request.form["itemNum"]
#     discount_val = request.form["discountVal"]

#     # do whatever
#     new_value = 1  # or something

#     from flask import jsonify
#     return jsonify(
#         {
#             itemNum=item_num,
#             newValue=new_value,
#         }
#     )

@app.route('/updateDiscount', methods=['POST'])
def updateDiscount():
    foodId = request.form["itemNum"]
    discount = request.form["discountVal"]
    database = Database()
    try:
        database.connect()
        price = inputDiscount(discount, foodId)
        newPrice = discount * price

    except Exception as e:
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)
        exit(1)

    return jsonify(
            {
                item_num: foodId,
                discountVal: newPrice
            } )
#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        stderr.write('Error: incorrect number of command-line arguments')
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    if argv[1].isdigit() == False:
        stderr.write('Error: port is not an integer')
        print('Usage: ' + argv[0] + ' integer port number')
        exit(1)
    app.run(host='localhost', port=int(argv[1]), debug=True)
