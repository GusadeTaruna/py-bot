import json
from flask import Flask, request, make_response, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import date
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

    parameters = req['queryResult']['parameters']

    if parameters.get('sapa'):
        balasan = 'SELAMAT DATANG! \n input ID karyawan untuk mulai'
        return {'fulfillmentText': balasan}

    elif parameters.get('kode'):
        inputan = req['queryResult']['queryText']
        sql = "select nama_karyawan from tb_karyawan where kode_karyawan=%s"
        cursor.execute(sql, (inputan,))
        records = cursor.fetchall()
        for row in records:
            bal = row[0]
        balasan = 'Selamat Datang %s\n\nKetik listperintah untuk menampilkan perintah yang tersedia' % bal
        return {'fulfillmentText': balasan}       

    elif parameters.get('perintah'):
        # balasan = '---- LIST PERINTAH YANG TERSEDIA----\n\n1. booking (Untuk pesan resource)\n2. lihatresource (Untuk melihat ketersediaan resource)\n3. lihatdatapinjam (Untuk melihat data peminjaman resource)'
        response = {
            'fulfillmentMessages': [
                {
                    "card": {
                        "title": "LIST PERINTAH",
                        "buttons": [
                            {
                                "text": "Booking (Untuk pesan resource)",
                                "postback": "booking"
                            },
                            {
                                "text": "lihatresource (Untuk melihat ketersediaan resource)",
                                "postback": "lihatresource"
                            },
                            {
                                "text": "lihatdatapinjam (Untuk melihat data peminjaman resource)",
                                "postback": "lihatdatapinjam"
                            }
                        ]
                    }
                }
            ]
        }

        return response

    elif parameters.get('menusatu'):
        sql = "SELECT id,kode_resource,nama_resource FROM tb_resource"
        cursor.execute(sql)
        records = cursor.fetchall()
        st = ''
        for row in records:
            if row[0]==0:
                st = st + 'Kode: %s'%row[1]+', Nama: %s'%row[2]+"\n"
            else:
                st = st + 'Kode: %s'%row[1]+', Nama: %s'%row[2]+"\n"
        response = {
            "fulfillmentMessages": [
                {
                    "card": {
                        "title": "-- LIST RESOURCE TERSEDIA --\n(masukkan kode resource untuk booking resource yang diinginkan)\n",
                        "subtitle": st
                    },
                },
            ],
        }
        return response

    elif parameters.get('kodepinjam'):
        kodeResource = req['queryResult']['queryText']
        sql = "INSERT INTO tb_pinjam_resource (tanggal_peminjaman, kode_resource) VALUES (%s, %s)"
        cursor.execute(sql, (date.today().strftime("%Y-%m-%d"), kodeResource))
        mySQLconnection.commit()
        return {'fulfillmentText': 'DATA BOOKING BERHASIL DIBUAT !\n\nKetik listperintah untuk melihat daftar perintah yang tersedia'}

    elif parameters.get('resource'):
        sql = "SELECT id,kode_resource,nama_resource FROM tb_resource"
        cursor.execute(sql)
        records = cursor.fetchall()
        st = ''
        for row in records:
            if row[0]==0:
                st = st + 'Kode: %s'%row[1]+', Nama: %s'%row[2]+"\n"
            else:
                st = st + 'Kode: %s'%row[1]+', Nama: %s'%row[2]+"\n"
        balasan = {
            "fulfillmentMessages": [
                {
                    "card": {
                        "title": "--- LIST RESOURCE ---\n\n(Ketik listperintah untuk kembali ke awal)\n",
                        "subtitle": st,
                    },
                },
            ],
        }
        return balasan

    elif parameters.get('listpinjam'):
        sql = "SELECT id,kode_karyawan,kode_resource,tanggal_peminjaman FROM tb_pinjam_resource"
        cursor.execute(sql)
        records = cursor.fetchall()
        st = ''
        for row in records:
            if row[0]==0:
                st = st + 'Kode Karyawan: %s\n'%row[1]+',Kode resource: %s\n'%row[2]+',Tanggal Pinjam : %s\n'%row[3]+"\n"
            else:
                st = st + 'Kode Karyawan: %s\n'%row[1]+',Kode resource: %s\n'%row[2]+',Tanggal Pinjam : %s\n'%row[3]+"\n"
        balasan = {
            "fulfillmentMessages": [
                {
                    "card": {
                        "title": "--- DATA BOOKING RESOURCE ---\n\n(Ketik listperintah untuk kembali ke awal)\n",
                        "subtitle": st,
                    },
                },
            ],
        }
        return balasan

    else:
        balasan = 'Inputan tidak dikenali\nCoba input kembali'
        return {'fulfillmentText': balasan}
    #AKHIR INTENT PROSESBOOKING
    # else:
    #     return {'fulfillmentText': 'anda mungkin salah ketik\nCoba input kembali'}


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
