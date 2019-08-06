import pymysql
from jinja2 import Template
import os
import time
from PIL import Image
from multiprocessing import Process
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

def FileRemove(Remove_Path, Remove_Name):
  remove = Remove_Path + Remove_Name + '.pdf'
  if os.path.exists(remove):
    os.remove(remove)
    print('Old PDF Removed')

def HercToPNG():
  Herc = '/var/www/Flask/static/Hercules.png'
  Herc = open(Herc, 'rb').read()
  Herc = base64.b64encode(Herc)
  Herc = Herc.decode('ascii')
  print('Herc')
  return Herc

def RenderHTML(html_Path, t, DATE, items,Name, Introduction, HercPath):
  with open(html_Path + Name + '.html', 'w') as f:
          f.write(t.render(items = items, DATE=DATE, Introduction = Introduction, HercPath = HercPath))
          f.close()

def PDFGEN(css_Path, html_Path, pdf_Path,Name ):
  if not os.path.exists(pdf_Path):
    os.makedirs(pdf_Path)
  HTML(html_Path + Name + '.html').write_pdf(pdf_Path + "/" + Name + ".pdf", stylesheets=[css_Path])
  print("Removing HTML")
  os.remove(html_Path + Name + '.html')

def imgToPNG(items):
  images = []
  for item in items:
    path = '/var/www/Flask/static/'
    PNGPath = "/var/www/Flask/ReportGenerator/PNG/"
    name = item['Receipt']
    imageName = name.split('.')
    imageName = imageName[0]
    png = PNGPath + imageName + ".png"
    if name != '' and not os.path.exists(png):
      image = path + name
      image = Image.open(image)
      images.append(imageName)
      new_height = 600
      new_width = 400
      image = image.resize((new_width, new_height), Image.ANTIALIAS)
      image.save(png,optimize=True,quality=100)
    try:
      image = open(png, 'rb').read()
      image = base64.b64encode(image)
      image = image.decode('ascii')
      item['Receipt'] = image

    except:
      image = ''
  return items

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





