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
    # build a request object
# def MySQL(querry):
#     try:
#         mySQLconnection = mysql.connector.connect(host='www.db4free.net',
#                     database='db_resource',
#                     user='gusade',
#                     password='gusade09')
#         sql_select_Query = querry
#         cursor = mySQLconnection .cursor()
#         cursor.execute(sql_select_Query)
#         records = cursor.fetchall()
#         return records

#     except Error as e :
#         print ("Error while connecting to MySQL", e)

#     finally:
#         if(mySQLconnection .is_connected()):
#             mySQLconnection.close()
#             print("MySQL connection is closed")

def MySQL(querry):
    try:
        mySQLconnection = mysql.connector.connect(host='www.db4free.net',
                    database='db_resource',
                    user='gusade',
                    password='gusade09')
        sql_select_Query = querry
        cursor = mySQLconnection .cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        return records

    except Error as e :
        print ("Error while connecting to MySQL", e)

    finally:
        if(mySQLconnection .is_connected()):
            mySQLconnection.close()
            print("MySQL connection is closed")



def cekKaryawan(req)
    parameters = req['queryResult']['parameters']
    inputan = req['queryResult']['queryText']
        if parameters.get('kode'):
            # if str(parameters.get('ucapan')) == str('Hai'.lower()):
            sql = MySQL("select nama_karyawan from tb_karyawan where kode_karyawan={}".format(inputan))
            for row in records: 
                bal = row[0]
            return'Selamat Datang %s\nKetik listperintah untuk menampilkan perintah yang tersedia' % bal
        else:
            return 'ID Karyawan tidak dikenali\nCoba input lagi'

    

# create a route for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    # return response
    req = request.get_json(force=True)


    # fetch action from json
    action = req['queryResult']['action']

    #AWAL INTENT SAPA
    if action == 'karyawan':
        res = cekKaryawan(req)

    # return a fulfillment response
    #AKHIR INTENT 


    else:
        return {'fulfillmentText': 'not'}


    # return make_response(jsonify(results()))
    return make_response(jsonify({"fulfillmentText": res}))

# run the app
if __name__ == '__main__':
   app.run()
