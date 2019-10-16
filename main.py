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


    try:
        mySQLconnection = mysql.connector.connect(host='www.db4free.net',
                    database='db_resource',
                    user='gusade',
                    password='gusade09')
        cursor = mySQLconnection .cursor()

    except Error as e :
        print ("Error while connecting to MySQL", e)


    # fetch action from json
    action = req['queryResult']['action']



    #AWAL INTENT cekKaryawan
    if action == 'karyawan': 
    # return a fulfillment response
        parameters = req['queryResult']['parameters']
        inputan = req['queryResult']['queryText']
        if parameters.get('kode'):
            # if str(parameters.get('ucapan')) == str('Hai'.lower()):
            sql = "select nama_karyawan from tb_karyawan where kode_karyawan=%s"
            cursor.execute(sql, (inputan,))
            records = cursor.fetchall()
            for row in records:
                bal = row[0]
            balasan = 'Selamat Datang %s\nKetik listperintah untuk menampilkan perintah yang tersedia' % bal
            return {'fulfillmentText': balasan}
        else:
            return {'fulfillmentText': 'ID Karyawan tidak dikenali\nCoba input lagi'}
    #AKHIR INTENT cekKaryawan




    #AWAL INTENT DAFTAR
    elif action == 'daftar':
        parameters = req['queryResult']['parameters']
        # inputan = req['queryResult']['queryText']
        if parameters.get('perintah'):
            balasan = '---- LIST PERINTAH YANG TERSEDIA----\n\n1. booking (Untuk pesan resource)\n2. lihatresource (Untuk melihat ketersediaan resource)\n3. lihatdatapinjam (Untuk melihat data peminjaman resource)'
            return {'fulfillmentText': balasan}
        else:
            balasan = 'Inputan yang anda masukkan tidak dikenali!\nKetik list untuk melihat daftar perintah yang tersedia'
            return {'fulfillmentText': balasan}
    #AKHIR INTENT SAPA




    #AWAL INTENT PROSESBOOKING
    elif action == 'pesan':
        parameters = req['queryResult']['parameters']
        # inputan = req['queryResult']['queryText']
        if parameters.get('booking'):
            if str(parameters.get('booking')) == str('Booking'.lower()):
                queryR = "select kode_resource,nama_resource from tb_resource"
                cursor.execute(queryR)
                records = cursor.fetchall()
                for row in records:
                    kodeR = row[0]
                    namaR = row[1]
                    rep = 'Resource yang ada :\n%s '% namaR+'(%s'% kodeR+')\n\n Masukkan kode resource yang ingin di booking'
                return {'fulfillmentText': rep}
            else:
                balasan = 'Inputan yang anda masukkan tidak dikenali!\nKetik list untuk melihat daftar perintah yang tersedia'
                return {'fulfillmentText': balasan}
    #AKHIR INTENT PROSESBOOKING


    #AWAL INTENT PROSESBOOKING
    elif action == 'menusatu': 
    # return a fulfillment response
        parameters = req['queryResult']['parameters']
        inputan = req['queryResult']['queryText']
        if parameters.get('kodepinjam'):
            # if str(parameters.get('ucapan')) == str('Hai'.lower()):
            sql = "INSERT INTO tb_pinjam_resource (kode_resource) VALUES (%s)"
            cursor.execute(sql, (inputan,))
            mySQLconnection.commit()
            return {'fulfillmentText': 'Masukkan tanggal mulai pinjam'}
        else:
            return {'fulfillmentText': 'ID Karyawan tidak dikenali\nCoba input lagi'}
    #AKHIR INTENT PROSESBOOKING


    else:
        return {'fulfillmentText': 'not'}


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


    

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()
