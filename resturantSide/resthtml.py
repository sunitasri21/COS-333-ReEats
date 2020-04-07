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

app = Flask(__name__,  template_folder='.')

@app.route('/', methods=['GET'])
def searchResults():
    restName = str(request.args.get('restName')) or ""
    discount = request.args.get('discount', default=1) 
     
    database = Database()
    try:
        database.connect()
        searchResults = database.menuSearch(restName)

    except Exception as e:
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)
        exit(1)


    database.disconnect()

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

@app.route('/updateDiscount', methods=['POST'])
def updateDiscount():
    foodId = request.form["itemNum"]
    discount = request.form["discountVal"]
    database = Database()
    try:
        database.connect()
        price = database.inputDiscount(discount, foodId)

    except Exception as e:
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)
        exit(1)

    newPrice = (1 - float(discount)) * float(price)
    return jsonify(
            {
                "itemNum": foodId,
                "discountVal": newPrice
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
