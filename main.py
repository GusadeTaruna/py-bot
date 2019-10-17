import json
from flask import Flask, request, make_response, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import date
import calendar


# initialize the flask app
app = Flask(__name__)

try:
    mySQLconnection = mysql.connector.connect(host='www.db4free.net',
                database='db_resource',
                user='gusade',
                password='gusade09')
    cursor = mySQLconnection .cursor()

except Error as e :
    print ("Error while connecting to MySQL", e)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response

    req = request.get_json(silent=True, force=True)

    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    if action == 'sapaan':
        return awal_cakap(req)

    elif action == 'karyawan':
        return cek_karyawan(req)

    elif action == 'daftar':
        return list_perintah(req)

    elif action == 'pesan':
        return menu_satu(req)

    elif action == 'book':
        return proses_menu_satu(req)

    elif action == 'daftarResource':
        return menu_dua(req)

    elif action == 'pinjaman':
        return menu_tiga(req)

    else:
        return undefined_input()

    return jsonify(request.get_json())


def awal_cakap(req):
    parameters = req['queryResult']['parameters']
    if parameters.get('sapa'):
        response = {
            'fulfillmentText': "SELAMAT DATANG! \ninput ID karyawan untuk mulai"
        }
        return response


def cek_karyawan(req):
    parameters = req['queryResult']['parameters']
    if parameters.get('kode'):
        inputan = req['queryResult']['queryText']
        sql = "select nama_karyawan from tb_karyawan where kode_karyawan=%s"
        cursor.execute(sql, (inputan,))
        records = cursor.fetchall()
        for row in records:
            bal = row[0]
        response = {
            'fulfillmentText': "Selamat Datang {}\n\nKetik listperintah untuk menampilkan perintah yang tersedia".format(bal)
        }

        sql2 = "INSERT INTO tb_pinjam_resource (kode_karyawan) VALUES (%s)"
        cursor.execute(sql2, (inputan,))
        mySQLconnection.commit()

        return response


def list_perintah(req):
    parameters = req['queryResult']['parameters']
    if parameters.get('perintah'):
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


def menu_satu(req):
    parameters = req['queryResult']['parameters']
    if parameters.get('menusatu'):
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


def proses_menu_satu(req):
    parameters = req['queryResult']['parameters']
    if parameters.get('kodepinjam'):
        kodeResource = req['queryResult']['queryText']
        sql = "UPDATE tb_pinjam_resource SET tanggal_peminjaman = %s, kode_resource =  %s ORDER BY id DESC LIMIT 1"
        # sql = "INSERT INTO tb_pinjam_resource (tanggal_peminjaman, kode_resource) VALUES (%s, %s)"
        cursor.execute(sql, (date.today().strftime("%Y-%m-%d"), kodeResource))
        mySQLconnection.commit()
        sql2 = "SELECT * FROM tb_pinjam_resource ORDER BY id DESC LIMIT 1"
        cursor.execute(sql2)
        records = cursor.fetchall()
        st = ''
        for row in records:
            if row[0]==0:
                st = st + 'Kode Karyawan: %s\n'%row[1]+'Kode Resource: %s\n'%row[2]+'Tanggal Peminjaman: %s\n'%row[3]+"\n"
            else:
                st = st + 'Kode Karyawan: %s\n'%row[1]+'Kode Resource: %s\n'%row[2]+'Tanggal Peminjaman: %s\n'%row[3]+"\n"
        response = {
            "fulfillmentMessages": [
                {
                    "card": {
                        "title": "BOOKING BERHASIL DILAKUKAN\n(Ketik listperintah untuk kembali ke awal)\n\n--- DATA BOOKING ---",
                        "subtitle": st
                    },
                },
            ],
        }
        return response


def menu_dua(req):
    parameters = req['queryResult']['parameters']
    if parameters.get('resource'):
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
                        "subtitle": st
                    },
                },
            ],
        }
        return balasan


def menu_tiga(req):
    parameters = req['queryResult']['parameters']
    if parameters.get('listpinjam'):
        sql = "SELECT id,kode_karyawan,kode_resource,tanggal_peminjaman FROM tb_pinjam_resource WHERE kode_karyawan IS NOT NULL AND kode_resource IS NOT NULL AND tanggal_peminjaman IS NOT NULL"
        cursor.execute(sql)
        records = cursor.fetchall()
        st = ''
        for row in records:
            if row[0]==0:
                st = st + 'Kode Karyawan: %s\n'%row[1]+'Kode resource: %s\n'%row[2]+'Tanggal Pinjam : %s\n'%row[3]+"\n"
            else:
                st = st + 'Kode Karyawan: %s\n'%row[1]+'Kode resource: %s\n'%row[2]+'Tanggal Pinjam : %s\n'%row[3]+"\n"
        balasan = {
            "fulfillmentMessages": [
                {
                    "card": {
                        "title": "--- DATA BOOKING RESOURCE ---\n\n(Ketik listperintah untuk kembali ke awal)\n",
                        "subtitle": st
                    },
                },
            ],
        }
        return balasan


def undefined_input():
    response = {
        'fulfillmentText': "Inputan Salah, Coba input ulang"
    }
    return balasan


# run the app
if __name__ == '__main__':
   app.run()
