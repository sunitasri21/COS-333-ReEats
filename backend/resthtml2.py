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
import stripe
from flask_sqlalchemy import SQLAlchemy
import re
from flask_mail import Mail, Message

#-----------------------------------------------------------------------
##TODO: remove exit()
template_dir = os.path.join(os.path.dirname(__file__), '../frontend')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))
stripe.api_key = 'sk_test_AwX9JLUwBYsuh9qhVFQISrDL00WRZ6jKh4'

dev = False
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

if dev:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reeats.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cavaxcayvoqxdp:d738fe5b698af40d07276a90ec25bdbb24eb4b89bb984fa6af075828c3df7d5b@ec2-54-165-36-134.compute-1.amazonaws.com:5432/d4pdqjkun0inr5'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_sql = SQLAlchemy(app)

# -----------------------------------------------------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['TESTING'] = False
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'reeatsprinceton@gmail.com',
    MAIL_PASSWORD = 'reeats2021',
    MAIL_DEFAULT_SENDER = 'reeatsprinceton@gmail.com',
))
mail = Mail(app)
mail.init_app(app)
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
    searchResults = database.menuSearchUser(restName)
    for thing in searchResults:
        print('searchresults', thing.getId())
        print('searchresults', thing.getFood())

    database.updateExpiredDiscounts()
    print("hellosearchresults")


    foodList = request.cookies.get('foodList')
    print(foodList)

    # response.set_cookie('total', str(total_value))
    # response.set_cookie('orderId', orderid)
    # response.set_cookie('CHECKOUT_SESSION_ID', sessionId)

    try:
        searchResults2 = database.menuSearchUser(restName)
        for thing in searchResults:
            print('searchresults2', thing.getId())
            print('searchresults2', thing.getFood())

    except Exception as e:
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)

        template = jinja_env.get_template("errorPage.html")

        html = render_template(template, errorMessage = errorMsg)
        response = make_response(html)
        return response 
    
    if 'logged_in' in session:
        # User is loggedin show them the home page
        template = jinja_env.get_template("userFirstPage.html")    
        html = render_template(template, restaurant=searchResults2, discount=discount, username=session.get('username'))
        response = make_response(html)
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        else:
            return response     
# -----------------------------------------------------------------------
@app.route('/userabout', methods=['GET'])

def userabout():
    html = render_template('userAbout.html')
    response = make_response(html)
    return response
# -----------------------------------------------------------------------
@app.route('/restabout', methods=['GET'])

def restabout():
    html = render_template('restAbout.html')
    response = make_response(html)
    return response  
# -----------------------------------------------------------------------
@app.route('/about', methods=['GET'])

def about():
    html = render_template('defaultAbout.html')
    response = make_response(html)
    return response  
# -----------------------------------------------------------------------
@app.route('/restFP', methods=['GET'])
@login_required
def restPage():
    restName = str(request.args.get('restName')) or ""
    discount = float(request.args.get('discount', default=1))
     
    database = get_db()
    database.updateExpiredDiscounts()

    try:
        # database.connect()
        searchResults = database.menuSearch(restName)

    except Exception as e:
        # errorMsg =  str(e)
        # stderr.write("database error: " + errorMsg)
        # raise e
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)

        template = jinja_env.get_template("errorPage.html")

        html = render_template(template, errorMessage = errorMsg)
        response = make_response(html)
        return response 

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
    database.updateExpiredDiscounts()

    try:
        results = database.previewAllDiscounts()
        for result in results:
            print(result.getId())
            print(result.getFood())
            print(result.getPrice())
            print(result.getDiscount())
            print(result.getNewPrice())

    except Exception as e:
        # errorMsg =  str(e)
        # stderr.write("database error: " + errorMsg)
        # raise e
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)

        template = jinja_env.get_template("errorPage.html")

        html = render_template(template, errorMessage = errorMsg)
        response = make_response(html)
        return response 

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
    username = session.get('username')
    email = session.get('email')
    password = session.get('password')
    html = render_template('restAccount.html', username=username, email=email, password=password)

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
    html = render_template('userFeedback.html', message="")
    response = make_response(html)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response  
# -----------------------------------------------------------------------
@app.route('/restFeedback', methods=['GET'])
@login_required

def restFeedback():
    html = render_template('restFeedback.html', message="")
    response = make_response(html)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response  
# -----------------------------------------------------------------------
@app.route('/sendMail', methods=['GET', 'POST'])
@login_required

def sendMail():
    database = get_db()
    # data = request.get_json()

    # name = data["name"]
    # email = data["email"]
    # comment = data["message"]

    name = request.form["name"]
    email = request.form["email"]
    comment = request.form["text"]

    print("Name = " + str(name))
    print("Email = " + str(email))
    print("Comment = " + str(comment))

    # message = "Name: " + str(name) + "\n" + "Email: " + str(email) + "\n" + "Message: " + str(comment)

    msg = Message(comment,
                recipients=["reeatsprinceton@gmail.com"])
    
    msg.subject = "Message from " + str(name) + " (" + str(email) + ")" 
    msg.body = str(comment)

    mail.send(msg)
    
    thanks = "Thank you! We will get back to you shortly."

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('userFeedback.html', message=thanks)
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
@app.route('/sendMailRest', methods=['GET', 'POST'])
@login_required

def sendMailRest():
    database = get_db()
    # data = request.get_json()

    # name = data["name"]
    # email = data["email"]
    # comment = data["message"]

    name = request.form["name"]
    email = request.form["email"]
    comment = request.form["text"]

    print("Name = " + str(name))
    print("Email = " + str(email))
    print("Comment = " + str(comment))

    # message = "Name: " + str(name) + "\n" + "Email: " + str(email) + "\n" + "Message: " + str(comment)

    msg = Message(comment,
                recipients=["reeatsprinceton@gmail.com"])
    
    msg.subject = "Message from " + str(name) + " (" + str(email) + ")" 
    msg.body = str(comment)

    mail.send(msg)
    
    thanks = "Thank you! We will get back to you shortly."

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('restFeedback.html', message=thanks)
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
            session['username'] = restaurant[1]  
            session['password'] = restaurant[2]
            session['email'] = restaurant[3]
            session['id'] = restaurant[0]
            session['orderid'] = None
            session['restaurant_name'] = database.restaurant_search(restaurant[0])
            login_user(restUser)
            # Redirect to home page
            return redirect(url_for('restPage'))
        elif user:
            userUser = User(user[1], unhashed_password, user[0], True, None)
            session['logged_in'] = True
            session['id'] = user[0]
            session['orderid'] = None
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
        rest, user = database.account_search(username, password)
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
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorPage.html', errorMessage = "404: Page Not Found!"), 404
# -----------------------------------------------------------------------

@app.route('/updateDiscount', methods=['POST'])
def updateDiscount():
    foodId = request.form["itemNum"]
    quantity = request.form["quantity"]
    discount = request.form["discountVal"]
    startTime = request.form["startTime"]
    endTime = request.form["endTime"]
    database = get_db()
    try:
        database.inputDiscount(discount, quantity, foodId, startTime, endTime)

        # database.connect()
        newPrice = float(database.pullNewPrice(foodId))
        retVal = jsonify(
            itemNum=foodId,
            discountVal=newPrice
            )

    except Exception as e:
        # errorMsg =  str(e)
        # stderr.write("database error: " + errorMsg)
        # raise e
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)

        template = jinja_env.get_template("errorPage.html")

        html = render_template(template, errorMessage = errorMsg)
        response = make_response(html)
        return response 

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
        # errorMsg =  str(e)
        # stderr.write("database error: " + errorMsg)
        # raise e
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)

        template = jinja_env.get_template("errorPage.html")

        html = render_template(template, errorMessage = errorMsg)
        response = make_response(html)
        return response 

    print("bungun")

    return retVal, 400

# @app.route('/payment', methods=['POST'])
# def payment():
    # stripe.api_key = 'sk_test_AwX9JLUwBYsuh9qhVFQISrDL00WRZ6jKh4'

    # session2 = stripe.checkout.Session.create(
    #   payment_method_types=['card'],
    #   line_items=[{
    #     'name': 'T-shirt',
    #     'description': 'Comfortable cotton t-shirt',
    #     'images': ['https://example.com/t-shirt.png'],
    #     'amount': int(total_value*100),
    #     'currency': 'usd',
    #     'quantity': 1
    #   }],
    #   success_url='http://www.gmail.com',
    #   cancel_url='http://www.facebook.com',
    # )

    # CHECKOUT_SESSION_ID=session2["id"]
    # print('sessioncreated', session2)
    # print(session2['id'])


#-----------------------------------------------------------------------
@app.route('/confirmationPage', methods=['GET','POST'])
@login_required
def confirmationPage():
    print("CONFIRMATION PAGE")
    print(request.referrer)

    prevURL = request.referrer
    parts = prevURL.split("/")
    prevPage = parts[3]

    if prevPage == "userFP":
        check_list = request.form.getlist("check_list[]")
        if len(check_list) == 0:
            return redirect(url_for('searchResults'))
        print(check_list)
        database = get_db()

        food_list = []
        total_value = 0

        if session['orderid'] == None:
            orderid = createOrderId()
            session['orderid'] = orderid
        else:
            orderid = session['orderid']   

        for value in check_list:
            try:
                # database.connect()
                newPrice = database.pullNewPrice(value)
                realval = database.pullQuantity(value)
                name = "item" + str(value) + "_quantity"
                quantity = request.form[name]
                # print("q: " + str(quantity))
                foodName = database.pullName(value)
                total_value = float(total_value) + float(quantity) * float(newPrice)
                database.updateQuantity(quantity, value)
                userid = session['id']
                confirmed = 1
                # response.set_cookie('foodList', str(value))
                session[value] = float(realval)
                database.inputOrderId(userid, newPrice, quantity, value, foodName, orderid, confirmed)
                food_list.append((value, newPrice, foodName, float(quantity)))
                foodid = str(value)
                print(value)

            except Exception as e:
                # errorMsg =  str(e)
                # stderr.write("database error: " + errorMsg)
                # raise e

                errorMsg =  str(e)
                stderr.write("database error: " + errorMsg)

                template = jinja_env.get_template("errorPage.html")

                html = render_template(template, errorMessage = errorMsg)
                response = make_response(html)
                return response 

    else:
        database = get_db()
        orderid = request.cookies.get('orderId')
        userid = session['id']
        print("userid = " + str(userid))
        confirmed = 1 

        try:
            results, total_value = database.confirmedOrder(userid, orderid, confirmed)

        except Exception as e:
            # errorMsg =  str(e)
            # stderr.write("database error: " + errorMsg)
            # raise e  
            errorMsg =  str(e)
            stderr.write("database error: " + errorMsg)

            template = jinja_env.get_template("errorPage.html")

            html = render_template(template, errorMessage = errorMsg)
            response = make_response(html)
            return response 

        print(len(results))

        check = True
        food_list = []

        for result in results:
            value = result.getId()
            newPrice = result.getNewPrice()
            foodName = result.getFood()
            quantity = result.getQuantity()
            print("quantity in results: " + str(quantity))
            if quantity != 0:
                check = False 
            food_list.append((value, newPrice, foodName, float(quantity)))

        if check:
            return redirect(url_for('login'))

    template = jinja_env.get_template("userConfirmation.html")
    # template2 = jinja_env.get_template("qrCodePage.html")

    url = "'https://reeats-test1.herokuapp.com/qrReroute?userid=" + str(userid) + "&orderid=" + str(orderid) + "'" + "&amp;size=100x100"

    html = render_template(template, foodList = food_list, total = total_value, orderId = orderid)
    # html2 = render_template(template2,foodList = food_list, total = total_value, orderid = url )
    response = make_response(html)
    # response.set_cookie('foodList', json_dumps(food_list))
    # response.set_cookie('total', str(total_value))
    response.set_cookie('orderId', orderid)

    # response.set_cookie('userId', userid)
    response.set_cookie('userId', str(userid))

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response

#-----------------------------------------------------------------------
@app.route('/globalCart', methods=['GET', 'POST'])
@login_required
def globalCart():
    database = get_db()
    orderid = request.cookies.get('orderId')
    userid = session['id']
    print("userid = " + str(userid))
    confirmed = 1 

    try:
        results, total_value = database.confirmedOrder(userid, orderid, confirmed)

    except Exception as e:
        # errorMsg =  str(e)
        # stderr.write("database error: " + errorMsg)
        # raise e  
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)

        template = jinja_env.get_template("errorPage.html")

        html = render_template(template, errorMessage = errorMsg)
        response = make_response(html)
        return response 

    print(len(results))

    check = True
    food_list = []

    for result in results:
        value = result.getId()
        newPrice = result.getNewPrice()
        foodName = result.getFood()
        quantity = result.getQuantity()
        print("quantity in results: " + str(quantity))
        if quantity != 0:
            check = False 
        food_list.append((value, newPrice, foodName, float(quantity)))

    template = jinja_env.get_template("userConfirmation.html")
    # template2 = jinja_env.get_template("qrCodePage.html")

    url = "https://api.qrserver.com/v1/create-qr-code/?data=" + orderid + "&amp;size=100x100"

    html = render_template(template, foodList = food_list, total = total_value, orderId = orderid)
    # html2 = render_template(template2,foodList = food_list, total = total_value, orderid = url )
    response = make_response(html)
    # response.set_cookie('foodList', json_dumps(food_list))
    # response.set_cookie('total', str(total_value))
    response.set_cookie('orderId', orderid)
    # response.set_cookie('userId', str(userid))

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response

#-----------------------------------------------------------------------
@app.route('/confirmationPageReloaded', methods=['POST'])
@login_required
def confirmationPageReloaded():
    database = get_db()
    data = request.get_json()
    print(data)

    foodName = data["name"]
    newPrice = data["price"]
    quantity = data["quantity"]
    orderid = data['orderId']
    foodid = data["foodId"]

    print("foodName: " + str(foodName))
    print("newPrice: " + str(newPrice))
    print("quantity: " + str(quantity))
    print("orderid: " + str(orderid))
    print("foodid: " + str(foodid))

    addQuantity = data["addQuantity"]
    subtractQuantity = data["subtractQuantity"]
    remove = data["remove"]

    print("remove = " + str(remove))

    print("CONFIRMATION PAGE RELOADED QUANTITY")

    print("resthtml: quantity = " + str(quantity))
    userid = session['id']
    confirmed = 0
    database.inputOrderId(userid, newPrice, quantity, foodid, foodName, orderid, confirmed)
    database.addQuantity(quantity, foodid)

    try:
        results, total_value = database.confirmedOrder(userid, orderid, 1)

    except Exception as e:
        # errorMsg =  str(e)
        # stderr.write("database error: " + errorMsg)
        # raise e  
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)

        template = jinja_env.get_template("errorPage.html")

        html = render_template(template, errorMessage = errorMsg)
        response = make_response(html)
        return response 

    print("RESULTS")
    for box in results:
        print(box.getId())

    template = jinja_env.get_template("removeItem.html")

    html = render_template(template, foodList = results, total = total_value)
    # html2 = render_template(template2,foodList = food_list, total = total_value, orderid = url )
    response = make_response(html)
    
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response

#-----------------------------------------------------------------------
@app.route('/confirmationPageReloadedQuantity', methods=['POST'])
@login_required
def confirmationPageReloadedQuantity():
    database = get_db()
    data = request.get_json()
    print(data)

    foodName = data["name"]
    newPrice = data["price"]
    quantity = data["quantity"]
    orderid = data['orderId']
    foodid = data["foodId"]

    originalQuantity = database.pullQuantity(foodid)
    totalQuantity = originalQuantity + quantity 

    print("foodName: " + str(foodName))
    print("newPrice: " + str(newPrice))
    print("quantity: " + str(quantity))
    print("orderid: " + str(orderid))
    print("foodid: " + str(foodid))

    addQuantity = data["addQuantity"]
    subtractQuantity = data["subtractQuantity"]
    remove = data["remove"]

    print("remove = " + str(remove))

    print("CONFIRMATION PAGE RELOADED QUANTITY")

    print("Currquant = " + quantity)
    print("Total = " + str(session[foodid]))

    if float(quantity) < session[foodid]:
        if addQuantity == "+":
            quantity = str(int(quantity) + 1)
    
    if int(quantity) > 1:
        if subtractQuantity == "-":
            quantity = str(int(quantity) - 1)

    print("resthtml: quantity = " + str(quantity))
    userid = session['id']
    confirmed = 1
    database.inputOrderId(userid, newPrice, quantity, foodid, foodName, orderid, confirmed)

    try:
        results, total_value = database.confirmedOrder(userid, orderid, confirmed)

    except Exception as e:
        # errorMsg =  str(e)
        # stderr.write("database error: " + errorMsg)
        # raise e  
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)

        template = jinja_env.get_template("errorPage.html")

        html = render_template(template, errorMessage = errorMsg)
        response = make_response(html)
        return response 

    print(len(results))

    html = str(quantity) + " " + str(total_value) + " " + str(newPrice)
    # html2 = render_template(template2,foodList = food_list, total = total_value, orderid = url )
    response = make_response(html)
    
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response
#-----------------------------------------------------------------------
@app.route('/checkoutSession', methods=['POST'])
def checkoutSession():
    data = request.get_json()

    username=session['email']
    total_value = data['total_value']
    total_value = total_value[6:]
    print(data)
    userid = session['id']
    orderid = request.cookies.get('orderId')
    print(orderid)

    session2 = stripe.checkout.Session.create(
      payment_method_types=['card'],
    #   receipt_email=['username'],
      line_items=[{
        'name': 'Your Order Total',
        'images': ["https://www.natrajindiancuisinevietnam.com/img/slider/slide01.jpg"],
        'amount': int(float(total_value)*100),
        'currency': 'usd',
        'quantity': 1
      }],

      metadata= {
        "userid": userid, 
        "orderid": orderid
        },
      success_url='https://reeats-test1.herokuapp.com/qrCodePage',
      cancel_url='https://reeats-test1.herokuapp.com/userFP'
      # success_url='http://reeats-test3.herokuapp.com/qrCodePage',
      # cancel_url='http://reeats-test3.herokuapp.com/userFP'
    )

    sessionId = session2["id"]
    
    html = sessionId

    response = make_response(html)

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response
#-----------------------------------------------------------------------
@app.route('/qrCodePage', methods=['GET'])
@login_required
def qrCodePage():
    # orderid = request.form["orderId"]
    # orderid = request.cookies.get('orderId')

    database = get_db()

    results = []
    total_value = 0

    userid = session['id']
    orderid = session['orderid']
    # confirmed = 1

    # try:
    #     results, total_value = database.confirmedOrder(userid, orderid, confirmed)

    # except Exception as e:
    #     errorMsg =  str(e)
    #     stderr.write("database error: " + errorMsg)
    #     raise e  
    # print(total_value)

    template2 = jinja_env.get_template("qrCodePage.html")

    url = "https://api.qrserver.com/v1/create-qr-code/?data=" + "https://reeats-test1.herokuapp.com/qrReroute?id=" + str(userid) + "_" + str(orderid) + "&amp;size=100x100"
    print(url)
    url2 = "https://reeats-test1.herokuapp.com/qrReroute?id=" + str(userid) + "_" + str(orderid)

    # for result in results:
    #     newPrice = result.getNewPrice()
    #     quantity = result.getQuantity()
    #     foodid = result.getId()
    #     foodName = result.getFood()
    #     orderid = result.getOrderId()
    #     confirmed = 0
    #     database.inputOrderId(userid, newPrice, quantity, foodid, foodName, orderid, confirmed)
    #     print(userid, newPrice, quantity, foodid, foodName, orderid, confirmed)
    
    print("REMOVED EVERYTHING")

    session['orderid'] = None

    html2 = render_template(template2,foodList = results, total = total_value, orderid = url, url2 = url2)
    response2 = make_response(html2)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response2

#-----------------------------------------------------------------------

@app.route('/qrReroute', methods=['GET'])
@login_required
def qrReroute():
    # orderid = request.form["orderId"]
    # orderid = request.cookies.get('orderId')
    # if confirmedFood_list == None:
    #     confirmedFood_list = []
    # print(confirmedFood_list)
    id1 = request.args.get('id')
    ids = id1.split("_")
    userid = ids[0]
    orderid = ids[1]
    
    database = get_db()
    results = []
    total_value = 0

    try:
        results, total_value = database.paidOrder(userid, orderid)
        for result in results:
            print('paidorder', result.getId())

    except Exception as e:
        # errorMsg =  str(e)
        # stderr.write("database error: " + errorMsg)
        # raise e  
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)

        template = jinja_env.get_template("errorPage.html")

        html = render_template(template, errorMessage = errorMsg)
        response = make_response(html)
        return response 

    template2 = jinja_env.get_template("qrReroute.html")

    # figure out how to get order id from a url

    # url = "https://api.qrserver.com/v1/create-qr-code/?data=" + "http://localhost:12345/qrReroute" + orderid + "&amp;size=100x100"

    html2 = render_template(template2,foodList = results, total = total_value)
    response2 = make_response(html2)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return response2



#-----------------------------------------------------------------------
@app.route('/restOrders', methods=['GET'])
@login_required
def restOrders():
    database = get_db()
    results = []
    total_value = 0

    try:
        results, total_value = database.allPaidOrders()
        for result in results:
            print('paidorder', result.getId())

    except Exception as e:
        # errorMsg =  str(e)
        # stderr.write("database error: " + errorMsg)
        # raise e  
        errorMsg =  str(e)
        stderr.write("database error: " + errorMsg)

        template = jinja_env.get_template("errorPage.html")

        html = render_template(template, errorMessage = errorMsg)
        response = make_response(html)
        return response 

    template2 = jinja_env.get_template("allOrders.html")

    # figure out how to get order id from a url

    # url = "https://api.qrserver.com/v1/create-qr-code/?data=" + "http://localhost:12345/qrReroute" + orderid + "&amp;size=100x100"

    html2 = render_template(template2,foodList = results, total = total_value)
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

@app.route("/webhooks", methods=["POST"])
def webhooks():
    # webhook_secret = "whsec_BUPGTfDOv2mIaP51MipyKfS0GfAOjw31" 
    # webhook_secret = "whsec_pu2iikEKy0aoYqCvSxBoqmKghbnL5bTz"
    # comment
    webhook_secret ="whsec_6iLpmaBG9GXUSXDiEZM51PkFQv7O4dUE"
    payload = request.data.decode("utf-8")
    received_sig = request.headers.get("Stripe-Signature", None)
    print("hellowebhooks")
    try:
        event = stripe.Webhook.construct_event(
            payload, received_sig, webhook_secret
        )
    except ValueError:
        print("Error while decoding event!")
        return "Bad payload", 400
    except stripe.error.SignatureVerificationError:
        print("Invalid signature!")
        return "Bad signature", 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        orderid = session['metadata']['orderid']
        userid = session['metadata']['userid']
        print(session)     
        print(orderid)
        print(userid)
        database = get_db()
        database.inputPaidOrder(userid, orderid)

    return "", 200
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
