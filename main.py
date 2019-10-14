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
@app.route('/webhook', methods=['GET','POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    try:
        action = reg['queryResult']['action']
    except AttributeError:
        return 'json error'

    if action == 'check_balance':
        res = check_balance(req)
    else:
        log.error('Unexpected action.')

    print('Action: ' + action)
    print('Response: ' + res)

    return make_response(jsonify({'fulfillmentText': res}))

def check_balance(req):
    """Returns a string containing text with a response to the user
    with the weather forecast or a prompt for more information
    Takes the city for the forecast and (optional) dates
    uses the template responses found in weather_responses.py as templates
    """
    parameters = req['queryResult']['parameters']

    print('Dialogflow Parameters:')
    print(json.dumps(parameters, indent=4))

    # validate request parameters, return an error if there are issues
    error, forecast_params = validate_params(parameters)
    if error:
        return error

    if parameters.get('account')
        response = 'respon1'

    return response


# run the app
if __name__ == '__main__':
   app.run()
