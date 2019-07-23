import pymysql
import imaplib
import email
import threading
import time
import socket
import re
import base64
from threading import Thread




db = pymysql.connect(host='192.168.0.20', port=3306, user='Test', password='Momrocks38', db='mydb',autocommit=True)
cur = db.cursor()
query = ("SELECT Date, TransID FROM tTransaction;")
cur.execute(query)
times=cur.fetchall()
for times in times:
    times = list(times)
    primarykey=str(times[1])
    split=times[0].split("/")
    month = split[0]
    day = split[1]
    year = split[2]
    date = year+"/"+month+"/"+day
    print("Primary key " + primarykey + " date " +date)
    db = pymysql.connect(host='192.168.0.20', port=3306, user='Test', password='Momrocks38', db='mydb', autocommit=True)
    cur = db.cursor((pymysql.cursors.DictCursor))
    sql = "UPDATE tTransaction SET  Date=(%s) WHERE TransID=(%s)"
    cur.execute(sql, (date,  primarykey))


