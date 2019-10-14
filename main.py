import json
from flask import Flask, request, make_response, jsonify
import mysql.connector
from mysql.connector import Error
import datetime
import calendar


# initialize the flask app
app = Flask(__name__)

# function for responses
# def results():
#     # build a request object
   

#     # return a fulfillment response
    

# create a route for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    try:
        action = reg['queryResult']['action']
    except AttributeError:
        return 'json error'
    if action == 'check_balance':
        reply = {'fulfillmentText': 'kec'}
    elif action == 'booking':
        reply = {'fulfillmentText': 'buks'}
    else:
        reply = {'fulfillmentText': 'hm'}
    # return response
    return jsonify(reply)

# run the app
if __name__ == '__main__':
   app.run()
