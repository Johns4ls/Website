import time
from datetime import timedelta
import datetime
from datetime import date
import pymysql
import smtplib
import sys
sys.path.append("/var/www/Flask/")
from Modules import Tlbx

def dates():
    Date = date.today().weekday()
    Month = time.strftime('%Y-%m')
    BeginMonth = Month + '-01'
    currentDate = date.fromtimestamp(time.time())
    Month = time.strftime('%m')
    Month = int(Month) + 1
    Year = time.strftime('%Y')
    newDate = date(int(Year), int(Month), 1)
    days = newDate - currentDate
    days = str(days)
    days = days.split(',')
    days = days[0]
    days = days.split(' ')
    days = days[0]
    print(days)
    currentDate = str(currentDate)
    return BeginMonth, currentDate, Date, days

def Balance():
    cur = Tlbx.dbConnect()
    query = ("Select SUM(Amount) FROM tTemporary")
    cur.execute(query)
    TempAmount = cur.fetchone()[0]
    query = ("Select SUM(Amount) FROM tTransaction")
    cur.execute(query)
    TransAmount = cur.fetchone()[0]
    Amount = TransAmount + TempAmount
    Amount = Amount
    return Amount

def incomplete():
    cur = Tlbx.dbConnect()
    query = ("Select COUNT(tempID) FROM tTemporary")
    cur.execute(query)
    Count = cur.fetchone()[0]
    Count = str(Count)
    return Count

def SendRentEmail(Amount, days):
    body = "Low balance, under $350 \n\nThe current balance is $" + Bal + ", and the rent has not been taken out.\n You have " + days + " days remaining before the next deposit."
    Tlbx.SendEmail(body)

def SendLowBalEmail():
    body = "Low Balance, under $100 \n\nThe current balance is $" + Bal + " and you have " + days + " days remaining before the next deposit."
    Tlbx.SendEmail(body)

def SendWeeklyEmail():
    if (Date == 4):
        body = "Weekly Update \n\nThe current Balance is $" + Bal + ". \nYou have " + Count + " incomplete transactions, and you have " + days + " days remaining before the next deposit."
        Tlbx.SendEmail(body)
    
 
BeginMonth, currentDate, Date, days = dates()
Bal = Balance()
Bal=('%.2f'%Bal)
Bal = str(Bal)
Count = incomplete()
if Date == Date:
    SendWeeklyEmail()
if (Date!= 4):
    Amount = Balance()
    if (Amount <= 350):
        cur = Tlbx.dbConnect()
        query = "Select * from tTransaction WHERE Name LIKE 'Housing' AND Date BETWEEN '" + BeginMonth + "' AND '" + currentDate +"';"
        cur.execute(query)
        try:
            Rent = cur.fetchone()[0]
        except:
            Rent = None
        if (Rent is None and Amount > 100):
            SendRentEmail(Amount, days)    

    if (Amount <= 100):
            SendLowBalEmail()

