import pymysql
from jinja2 import Template
import os
import time
from datetime import timedelta
import datetime
from datetime import date
import smtplib

def SendEmail(body):
    try:  
        gmail_user = 'johnsonandrew123198@gmail.com'  
        gmail_password = 'Momrocks38'
        sent_from = gmail_user  
        to = ['5132073777@vtext.com']  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        #Gmail will not send :
        body = body.replace(":","")
        server.sendmail(sent_from, to, body)
        server.close()
    except:
        print("Could Not Connect")


def dbConnect():
  db = pymysql.connect(host='127.0.0.1', port=3306, user='WebServer', password='Momrocks38', db='mydb',autocommit=True)
  cur = db.cursor()
  return cur
def dbConnectDict():
  db = pymysql.connect(host='127.0.0.1', port=3306, user='WebServer', password='Momrocks38', db='mydb',autocommit=True)
  cur = db.cursor(pymysql.cursors.DictCursor)
  return cur



def convertMonth(MONTH):

  if MONTH == '01':
    MONTH = 'January'
  if MONTH == '02':
    MONTH = 'February'
  if MONTH == '03':
    MONTH = 'March'
  if MONTH == '04':
    MONTH = 'April'
  if MONTH == '05':
    MONTH = 'May'
  if MONTH == '06':
    MONTH = 'June'
  if MONTH == '07':
    MONTH = 'July'
  if MONTH == '08':
    MONTH = 'August'
  if MONTH == '09':
    MONTH = 'September'
  if MONTH == '10':
    MONTH = 'October'
  if MONTH == '11':
    MONTH = 'November'
  if MONTH == '12':
    MONTH = 'December'
  return MONTH


def Balance():
    cur = dbConnect()
    query = ("Select SUM(Amount) FROM tTemporary")
    cur.execute(query)
    TempAmount = cur.fetchone()[0]
    query = ("Select SUM(Amount) FROM tTransaction")
    cur.execute(query)
    TransAmount = cur.fetchone()[0]
    try:
        balance = TransAmount + TempAmount
    except:
        balance = TransAmount
    if balance is not None:
        balance = ('%.2f' % balance)
    return balance

def dateConvert(Day, Month, Year):
    try:
        if (Day == "1"):
            Day = "01"
        if (Day == "2"):
            Day = "02"
        if (Day == "3"):
            Day = "03"
        if (Day == "4"):
            Day = "04"
        if (Day == "5"):
            Day = "05"
        if (Day == "6"):
            Day = "06"
        if (Day == "7"):
            Day = "07"
        if (Day == "8"):
            Day = "08"
        if (Day == "9"):
            Day = "09"

        # take second item and convert to mm

        if (Month == 'Jan'):
            Month = "01"
        if (Month == 'Feb'):
            Month = "02"
        if (Month == 'Mar' or Month == 'March'):
            Month = "03"
        if (Month == 'Apr' or Month == 'April'):
            Month = "04"
        if (Month == 'May'):
            Month = "05"
        if (Month == 'Jun' or Month == 'June'):
            Month = "06"
        if (Month == 'Jul' or Month == 'July'):
            Month = "07"
        if (Month == 'Aug'):
            Month = "08"
        if (Month == 'Sep' or Month == 'Sept'):
            Month = "09"
        if (Month == 'Oct'):
            Month = "10"
        if (Month == 'Nov'):
            Month = "11"
        if (Month == 'Dec'):
            Month = "12"

        # get third as year


        # put the parsed data in Date
        Date = Year + "/" + Month + "/" + Day
        return Date
    except:
        print("Couldn't get a date")





