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

    if action == 'sapa':
    # return a fulfillment response
        parameters = req['queryResult']['parameters']
        # inputan = req['queryResult']['queryText']
        if parameters.get('ucapan'):
            if str(parameters.get('ucapan')) == str('Hai'.lower()):
                balasan = 'Selamat datang di yumibot!\nKetik list untuk melihat daftar perintah yang tersedia'
                return {'fulfillmentText': balasan}
            else:
                balasan = 'Inputan yang anda masukkan tidak dikenali!\nKetik list untuk melihat daftar perintah yang tersedia'
                return {'fulfillmentText': balasan}

    elif action == 'daftar':
        parameters = req['queryResult']['parameters']
        # inputan = req['queryResult']['queryText']
        if parameters.get('perintah'):
            balasan = 'LIST PERINTAH YANG TERSEDIA\n1. booking (Untuk pesan resource)\n2. lihatresource (Untuk melihat ketersediaan resource)\n3. lihatdatapinjam (Untuk melihat data peminjaman resource)'
            return {'fulfillmentText': balasan}
        else:
            balasan = 'Inputan yang anda masukkan tidak dikenali!\nKetik list untuk melihat daftar perintah yang tersedia'
            return {'fulfillmentText': balasan}

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
