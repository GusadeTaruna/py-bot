import json
from flask import Flask, request, make_response, jsonify
import mysql.connector
from mysql.connector import Error
import datetime
import calendar


# initialize the flask app
app = Flask(__name__)

# function for responses
def results():
    # build a request object
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('result').get('action')
    except AttributeError:
        return 'json error'

    if action == 'check_balance':
        return {'cek'}
    elif action == 'booking':
        return {'books'}
    else:
        return {'webhook'}

    # return a fulfillment response
    

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()
