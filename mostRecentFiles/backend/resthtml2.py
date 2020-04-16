#!/usr/bin/env python

#-----------------------------------------------------------------------
# resthtml.py
# Author: Sunita Srivatsan
#-----------------------------------------------------------------------
import flask 
from sys import argv, stderr
from restdatabase2 import Database
from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for, session, abort
from flask import render_template, flash 
import jinja2
from sys import exit, argv, stderr
import os
from flask import jsonify
from flask import g

#-----------------------------------------------------------------------
##TODO: remove exit()
template_dir = os.path.join(os.path.dirname(__file__), '../frontend')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

# -----------------------------------------------------------------------

def create_app():
    app = Flask(__name__,  template_folder='../frontend')

    with app.app_context():
        get_db()

    return app

def connect_to_database():
    database = Database()
    database.connect()
    return database

def get_db():
    if 'db' not in g:
        g.db = connect_to_database()

    return g.db

app = create_app()

# -----------------------------------------------------------------------

@app.route('/', methods=['GET'])
def searchResults():
    restName = str(request.args.get('restName')) or ""
    discount = request.args.get('discount', default=1) 
      
    database = get_db()

    try:
        searchResults = database.menuSearchUser(restName)
        for thing in searchResults:
            print(thing.getId())
            print(thing.getFood())

    except Exception as e:
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)
        raise e

    template = jinja_env.get_template("userFirstPage.html")

    html = render_template(template, restaurant=searchResults, discount=discount)
    response = make_response(html)

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response  
# -----------------------------------------------------------------------
@app.route('/restFP', methods=['GET'])
def restPage():
    restName = str(request.args.get('restName')) or ""
    discount = request.args.get('discount', default=1) 
     
    database = get_db()

    try:
        # database.connect()
        searchResults = database.menuSearch(restName)

    except Exception as e:
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)
        raise e

    template = jinja_env.get_template("restFirstPage.html")

    html = render_template(template, restaurant=searchResults, discount=discount)
    response = make_response(html)

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response     

# -----------------------------------------------------------------------

@app.route('/checkoutPage', methods=['GET'])
def checkoutPage():
    database = get_db()
    try:
        results = database.previewAllDiscounts()
        for result in results:
            print(result.getId())
            print(result.getFood())
            print(result.getPrice())
            print(result.getDiscount())
            print(result.getNewPrice())




    except Exception as e:
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)
        raise e

    template = jinja_env.get_template("checkoutPage.html")

    html = render_template(template, items=results)
    response = make_response(html)

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response     
# -----------------------------------------------------------------------

# @app.route('/restFirstPage', methods=['GET'])
# def restFirstPage():
#     html = render_template('restFirstPage.html')
#     response = make_response(html)
#     return response

# -----------------------------------------------------------------------

@app.route('/accountPage', methods=['GET'])
def accountPage():
    html = render_template('accountPage.html')
    response = make_response(html)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response     
# -----------------------------------------------------------------------

@app.route('/feedbackPage', methods=['GET'])
def feedbackPage():
    html = render_template('feedbackPage.html')
    response = make_response(html)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response     
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']    
        # Check if account exists using MySQL
        database = Database()
        database.connect()
        restaurant, user = database.account_search(username, password)
        # If restaurant account exists in accounts table in out database
        if restaurant:
            # Create session data, we can access this data in other routes
            session['logged_in'] = True
            session['username'] = restaurant[1]  
            session['id'] = restaurant[0]
            session['restaurant_name'] = database.restaurant_search(restaurant[0])
            # Redirect to home page
            return redirect(url_for('restPage'))
        elif user:
            session['logged_in'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('searchResults'))
        else:          
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)    

# -----------------------------------------------------------------------
@app.route("/logout")
def logout():
    # Remove session data, this will log the user out
    session['logged_in'] = False
    session.pop('id', None)
    session.pop('username', None)
    session.pop('restaurant_name', None)
    # Redirect to login page
    return redirect(url_for('login'))

# -----------------------------------------------------------------------
@app.route('/login/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# -----------------------------------------------------------------------

@app.route('/updateDiscount', methods=['POST'])
def updateDiscount():
    foodId = request.form["itemNum"]
    discount = request.form["discountVal"]
    database = get_db()
    try:
        database.inputDiscount(discount, foodId)

        # database.connect()
        newPrice = database.pullNewPrice(foodId)
        retVal = jsonify(
            itemNum=foodId,
            discountVal=newPrice
            )

    except Exception as e:
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)
        raise e

    return retVal, 200
#-----------------------------------------------------------------------
@app.route('/getNewPrice', methods=['POST'])
def getNewPrice():
    foodId = request.form["itemNum"]
    database = get_db()
    try:
        # database.connect()
        newPrice = database.pullNewPrice(foodId)
        retVal = jsonify(
            itemNum=foodId,
            discountVal=newPrice
            )

    except Exception as e:
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)
        raise e

    print("bungun")

    return retVal, 400
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
@app.route('/confirmationPage', methods=['POST'])
def confirmationPage():
    check_list = request.form.getlist("check_list[]")
    print(check_list)
    database = get_db()

    food_list = []
    
    for value in check_list:
        try:
            # database.connect()
            newPrice = database.pullNewPrice(value)
            foodName = database.pullName(value)
            food_list.append((value, newPrice, foodName))
            print(value)

        except Exception as e:
            errorMsg =  str(e)
            stderr.write("database error: " + errorMsg)
            raise e

    template = jinja_env.get_template("confirmationPage.html")

    html = render_template(template, foodList = food_list)
    response = make_response(html)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response     
#-----------------------------------------------------------------------
@app.teardown_appcontext
def teardown_db(error):
    db = g.pop('db', None)

    if db is not None:
        db.disconnect()

if __name__ == '__main__':
    if len(argv) != 2:
        stderr.write('Error: incorrect number of command-line arguments')
        print('Usage: ' + argv[0] + ' port')
        raise Exception("incorrect number of args") 
    if argv[1].isdigit() == False:
        stderr.write('Error: port is not an integer')
        print('Usage: ' + argv[0] + ' integer port number')
        raise Exception("port is not an integer")
    app.secret_key = os.urandom(12)    
    app.run(host='localhost', port=int(argv[1]), debug=True)
