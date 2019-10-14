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
    req = request.get_json(force=True)

    # fetch action from json
    action = req['queryResult']['action']

    if action == 'check_balance':
    # return a fulfillment response
        return {'fulfillmentText': 'This is a response from webhook.'}
    elif action == 'booking':
    # return a fulfillment response
        return {'fulfillmentText': 'yes'}
    else:
        return {'fulfillmentText': 'not'}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()
