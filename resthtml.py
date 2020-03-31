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

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------
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

    html = render_template('restFirstPage.html', restaurant=searchResults, discount=discount)
    response = make_response(html)
    return response         

# # #-----------------------------------------------------------------------

# @app.route('/handleDiscount', methods=['GET'])
#  def handleDiscount():
#      discount = request.args.get('discount') or 1
#      if discount:
#          r = requests.get('http://localhost:55555')

#          soup = BeautifulSoup(r.content, 'lxml')

#          prices = soup.findAll('td', attrs={'name': 'price'})

#          for price in suggestions:
#              suggestions_list.append(suggestion.attrs['data'])
     
#      html = render_template(r,
#          prices=prices)
#      response = make_response(html) 
#      return response          

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
