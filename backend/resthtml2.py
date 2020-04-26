#!/usr/bin/env python

#-----------------------------------------------------------------------
# resthtml.py
# Author: Sunita Srivatsan
#-----------------------------------------------------------------------
import flask 
from sys import argv, stderr
from restdatabase2 import Database
from flask import Flask, request, make_response, redirect, url_for, session, abort
from flask import render_template, flash 
import jinja2
from sys import exit, argv, stderr
import os
from flask import jsonify
from flask import g
import random
from time import localtime, asctime, strftime
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin



#-----------------------------------------------------------------------
##TODO: remove exit()
template_dir = os.path.join(os.path.dirname(__file__), '../frontend')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

# -----------------------------------------------------------------------

def create_app():
    app = Flask(__name__,  template_folder='../frontend')
    app.secret_key = "WEFWEFGEWDNFEJNJK2938Rdnjenfcjv"


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

login_manager = LoginManager()
login_manager.init_app(app)
app.config['TESTING'] = False
# -----------------------------------------------------------------------
class User(UserMixin):
    def __init__ (self, username, password, userid, admin, email):
        self.username = username
        self.password = password
        self.id = userid 
        self.admin = admin
        self.email = email
# -----------------------------------------------------------------------
@app.route('/', methods=['GET'])
def firstPage():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('searchResults')) 

@app.route('/userFP', methods=['GET'])
@login_required

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
    
    if 'logged_in' in session:
        # User is loggedin show them the home page
        template = jinja_env.get_template("userFirstPage.html")    
        html = render_template(template, restaurant=searchResults, discount=discount, username=session['username'])
        response = make_response(html)
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        else:
            return response     
# -----------------------------------------------------------------------
@app.route('/restFP', methods=['GET'])
@login_required
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

@app.route('/restDiscount', methods=['GET'])
@login_required

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

    template = jinja_env.get_template("restDiscount.html")

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

@app.route('/restAccount', methods=['GET'])
@login_required

def restAccount():
    html = render_template('restAccount.html')
    response = make_response(html)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response     
# -----------------------------------------------------------------------

@app.route('/userAccount', methods=['GET'])
@login_required

def userAccount():
    username = session.get('username')
    email = session.get('email')
    password = session.get('password')
    html = render_template('userAccount.html', username=username, email=email, password=password)

    response = make_response(html)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response     
# -----------------------------------------------------------------------

@app.route('/userFeedback', methods=['GET'])
@login_required

def userFeedback():
    html = render_template('userFeedback.html')
    response = make_response(html)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response  
# -----------------------------------------------------------------------
@app.route('/restFeedback', methods=['GET'])
@login_required

def restFeedback():
    html = render_template('restFeedback.html')
    response = make_response(html)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response  
# -----------------------------------------------------------------------

@login_manager.user_loader
def load_user(id):
    database = get_db()
    restaurant, user = database.user_search(id)
    if restaurant:
        restUser = User(restaurant[1], restaurant[2], restaurant[0], True, None)
        return restUser
    if user:
        userUser = User(user[1], user[2], user[0], True, None)
        return userUser

# -----------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    database = get_db()
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        unhashed_password = request.form['password']    
        # Check if account exists using MySQL
        restaurant, user = database.account_search(username, unhashed_password)
        # If restaurant account exists in accounts table in out database
        if restaurant:
            restUser = User(restaurant[1], unhashed_password, restaurant[0], True, None)
            # Create session data, we can access this data in other routes
            session['logged_in'] = True
            session['username1'] = restaurant[1]  
            session['id'] = restaurant[0]
            session['restaurant_name'] = database.restaurant_search(restaurant[0])
            login_user(restUser)
            # Redirect to home page
            return redirect(url_for('restPage'))
        elif user:
            userUser = User(user[1], unhashed_password, user[0], True, None)
            session['logged_in'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            session['password'] = user[2]
            session['email'] = user[3]
            login_user(userUser)

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
    logout_user()
    # Redirect to login page
    return redirect(url_for('login'))

# -----------------------------------------------------------------------
@app.route('/login/register', methods=['GET', 'POST'])
def register():
    database = get_db()
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists in the database: 
        rest, user = database.account_search(username)
        # If account exists show error and validation checks
        if rest or user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            database.add_user(None, username, password, email)
            msg = 'You have successfully registered!'        
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# -----------------------------------------------------------------------

@app.route('/updateDiscount', methods=['POST'])
def updateDiscount():
    foodId = request.form["itemNum"]
    quantity = request.form["quantity"]
    discount = request.form["discountVal"]
    database = get_db()
    try:
        database.inputDiscount(discount, quantity, foodId)

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
def createOrderId():

    orderId           = ''
    characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    charactersLength = len(characters)
    for i in range(6):
        orderId += characters[int(random.random() * charactersLength)]
    return orderId
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
@app.route('/confirmationPage', methods=['POST'])
@login_required
def confirmationPage():
    check_list = request.form.getlist("check_list[]")
    if check_list == None:
        check_list = []
    print(check_list)
    database = get_db()

    food_list = []
    total_value = 0
    orderid = createOrderId()
    
    for value in check_list:
        try:
            # database.connect()
            newPrice = database.pullNewPrice(value)
            name = "item" + str(value) + "_quantity"
            quantity = request.form[name]
            foodName = database.pullName(value)
            food_list.append((value, newPrice, foodName, float(quantity)))
            total_value = total_value + float(quantity) * newPrice
            database.updateQuantity(quantity, value)
            userid = session['id']
            confirmed = 1
            database.inputOrderId(userid, newPrice, quantity, value, foodName, orderid, confirmed)
            print(value)

        except Exception as e:
            errorMsg =  str(e)
            stderr.write("database error: " + errorMsg)
            raise e

    template = jinja_env.get_template("UserConfirmation.html")
    # template2 = jinja_env.get_template("qrCodePage.html")

    url = "https://api.qrserver.com/v1/create-qr-code/?data=" + orderid + "&amp;size=100x100"

    html = render_template(template, foodList = food_list, total = total_value, orderId = orderid)
    # html2 = render_template(template2,foodList = food_list, total = total_value, orderid = url )
    response = make_response(html)
    # response2 = make_response(html2)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response

#-----------------------------------------------------------------------
@app.route('/qrCodePage', methods=['POST'])
@login_required
def qrCodePage():
    orderid = request.form["orderId"]
    print(orderid)
    # if confirmedFood_list == None:
    #     confirmedFood_list = []
    # print(confirmedFood_list)
    database = get_db()

    results = []
    total_value = 0

    userid = session['id']

    # orderid = createOrderId()

    confirmed = 1

    try:
        results, total_value = database.confirmedOrder(userid, orderid, confirmed)
        print(results)

    except Exception as e:
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)
        raise e  

    template2 = jinja_env.get_template("qrCodePage.html")

    url = "https://api.qrserver.com/v1/create-qr-code/?data=" + orderid + "&amp;size=100x100"

    html2 = render_template(template2,foodList = results, total = total_value, orderid = url)
    response2 = make_response(html2)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response2



#-----------------------------------------------------------------------
def createOrderId():
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    orderId = ""
    for i in range(6):
        orderId += letters[int(random.random()*len(letters))]
    return orderId
#-----------------------------------------------------------------------
# @app.route('/userCheckout', methods=['POST'])
# def userCheckoutPage():
#     check_list = request.form.getlist("check_list[]")
#     print(check_list)
#     database = get_db()
#     order_id = createOrderId()
#     user_id = session.get('id')
#     print(user_id)
#     food_list = []
#     total_value = 0
    
#     for value in check_list:
#         try:
#             # database.connect()
#             newPrice = database.pullNewPrice(value)
#             name = "item" + str(value) + "_quantity"
#             quantity = request.form[name]
#             foodName = database.pullName(value)
#             food_list.append((value, newPrice, foodName, float(quantity)))
#             total_value = total_value + float(quantity) * newPrice
#             database.updateQuantity(quantity, value)

#             database.inputOrderId(user_id, foodName, value, order_id, quantity, newPrice)
#             print(value)

#         except Exception as e:
#             errorMsg =  str(e)
#             stderr.write("database error: " + errorMsg)
#             raise e

#     template = jinja_env.get_template("userCheckout.html")

#     html = render_template(template)
#     response = make_response(html)
#     if not session.get('logged_in'):
#         return redirect(url_for('login'))
#     else:
#         return response     
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
