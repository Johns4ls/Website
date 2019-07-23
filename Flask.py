#Various imports
from flask import Flask, flash, render_template, send_from_directory
import pymysql
from flask import Flask, request, redirect, url_for, send_file, session
from werkzeug.utils import secure_filename
import os
import PIL
from PIL import Image, ExifTags
from datetime import date, datetime, timedelta
import sys
import time
from Modules import Tlbx, WebGenerate
from threading import Lock
from flask_socketio import SocketIO, emit
import psutil
import uptime
import math
import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol
import time
from twisted.internet import task
import socket
import subprocess
import select
from flask import Flask
from os import listdir
from os.path import isfile, join

#Set upload folder for receipt images, and set max upload size
UPLOAD_FOLDER = '/var/www/Flask/static/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.secret_key = 'some_secret'
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
_data = None
_Machine = None
_Command = None
_Message = None
_CPU = None
_RAM = None
_Uptime = None
_PlexState = None
_MinecraftState = None
_TVShowState = None
_MovieState = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
isConnected = False

@app.before_request
def before_request():
    print("Trying")
    global s
    global isConnected
    if isConnected == True:
        print("IsConnected")
        try:
            print("Closing")
            s.close()
            isConnected == False
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Closing Socket")
        except:
            print("Failed To Close Socket")
            isConnected == False
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Initial screen upon entering website.
@app.route("/")
def index():

    #Get the current balance
    balance = Tlbx.Balance()
        
    #Connect to the database to post number of incomplete transactions    
    cur = Tlbx.dbConnect()
    query = ("Select COUNT(tempID) FROM tTemporary")
    cur.execute(query)
    Transaction = cur.fetchone()[0]
    
    #A catch from testing to prevent a crash
    if Transaction is None:
        Transaction = "0"
        
    #Render the page
    return render_template('HomePage/index.html', balance = balance, Transaction = Transaction)

#Route to show the hercules icon
@app.route('/favicon.ico')
def favicon():

    #Return the directory of the image for use
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

#Render newpayment   
@app.route("/newpayment")
def NewPayment():
    return render_template('NewPayment/NewPayment.html', **locals())

#Render result
@app.route("/result", methods=['POST', 'GET'])
def result():
    #Request data from newpayment webpage
    name = ''
    Name = request.form['Name']
    Description = request.form['Description']
    WithdrawDeposit = request.form['WithdrawDeposit']
    Company = request.form['Company']
    Date = request.form['Date']
   
    #Split data since it is submitted as mm/dd/yyyy and convert to yyyy/mm/dd
    split = Date.split("-")
    month = split[0]
    day = split[1]
    year = split[2]
    Date = year + "-" + month + "-" + day
   
    #implemented required html tag to prevent crash if no amount
    Amount = request.form['Amount']
    Amount = float(Amount)
    Comments = request.form['Comments']
   
    # a check to ensure Amount will be positive or negative
    if (WithdrawDeposit == "Withdraw" or WithdrawDeposit == "withdraw"):
        Amount = (Amount * -1)
    if (WithdrawDeposit == "Deposit" or WithdrawDeposit == "deposit"):
        Amount = abs(Amount)
      
    # get data for new webpage, potentially unnecessary.
    request.get_data('Name')
    request.get_data('Description')
    request.get_data('WithdrawDeposit')
    request.get_data('Company')
    request.get_data('Amount')
    request.get_data('Comments')

    #if image isn't null, rotate the image and PIL automatically sheds off EXIF tag
    if request.files['file'].filename != '':
        image = Image.open(request.files['file'].stream)
        if hasattr(image, '_getexif'):
            orientation = 0x0112
            exif = image._getexif()
            if exif is not None:
                orientation = exif[orientation]
                rotations = {
                    3: Image.ROTATE_180,
                    6: Image.ROTATE_270,
                    8: Image.ROTATE_90
                }
                if orientation in rotations:
                    image = image.transpose(rotations[orientation])
        name = request.files['file'].filename
        path = 'C:/Users/johns/Google Drive/ProgrammingProjects/Python/Flask_Desktop/static/' + name

        #Does an optimization pass to compress without noticeably reducing quality
        image.save(path, "JPEG", optimize=True, quality=85)
    #Connect to database and commit data
    cur = Tlbx.dbConnectDict()
    query = ("INSERT INTO tTransaction (Name, Description, WithdrawDeposit, Company, Date, Amount, Comments, Receipt) VALUES ( %s, %s, %s, %s, %s, %s, %s,%s)")
    data = (Name, Description, WithdrawDeposit, Company, Date, Amount, Comments, name)
    cur.execute(query, data)
    request.get_data('image')

    #Convert date back to display mm-dd-yyyy
    Date = month + "-" + day + "-" + year
    request.get_data('Date')
    return render_template("NewPayment/result.html", Name=Name, Description=Description, WithdrawDeposit=WithdrawDeposit, Company=Company, Date=Date, Amount = Amount, Comments=Comments, image=name)


@app.route("/PickDate", methods=['POST', 'GET'])
def DatePicker():
    return(render_template("ReportGeneration/DatePicker.html"))

@app.route("/Andrew", methods=['POST', 'GET'])
def Andrew():
    Unoptimizedpath = '/var/www/Flask/static/Andrew/Unoptimized/'
    Optimizedpath = '/var/www/Flask/static/Andrew/Optimized/'
    Path = '/static/Andrew/Optimized/'
    #if image isn't null, rotate the image and PIL automatically sheds off EXIF tag, then saves the image as an optimized JPEG
    AndrewPics = [f for f in listdir(Unoptimizedpath) if isfile(join(Unoptimizedpath, f))]
    for idx, item in enumerate(AndrewPics):
        image = Image.open(Unoptimizedpath+item)
        if hasattr(image, '_getexif'):
            orientation = 0x0112
            exif = image._getexif()
            if exif is not None:
                orientation = exif[orientation]
                rotations = {
                    3: Image.ROTATE_180,
                    6: Image.ROTATE_270,
                    8: Image.ROTATE_90
                }
                if orientation in rotations:
                    image = image.transpose(rotations[orientation])
        path = Optimizedpath + item
        print("The save path is " + path)

        #Does an optimization pass to compress without noticeably reducing quality
        image.save(path, "JPEG", optimize=True, quality=85)
        os.remove(Unoptimizedpath+item)
    AndrewPics = [f for f in listdir(Optimizedpath) if isfile(join(Optimizedpath, f))]
    for idx, item in enumerate(AndrewPics):
        AndrewPics[idx] = join(Path,item)
    return(render_template("Andrew/Andrew.html", AndrewPics=AndrewPics))

@app.route("/ReportGeneration", methods=['POST', 'GET'])
def RedirectPDF():
    AllTimePath = "ReportGenerator/Reports/All-Time/Andrews Complete Financial Report.pdf"
    AllTimeName = "Andrews Complete Financial Report.pdf"
    YearlyPath = "var/www/Flask/ReportGenerator/Reports/"
    InitialDate = request.form['InitialDate']
    FinalDate = request.form['FinalDate']
    FirstDate = InitialDate.split("/")
    InDay = int(FirstDate[1])
    InMonth = int(FirstDate[0])
    InYear = int(FirstDate [2])
    InDate = date(InYear, InMonth, InDay)
    CurrentDate = FinalDate.split("/")
    CurDay = int(CurrentDate[1])
    CurMonth = int(CurrentDate[0])
    CurYear = int(CurrentDate[2])
    CurDate = date(CurYear,CurMonth,CurDay)
    time = CurDate - InDate 
    if(time.days >=366):
        return send_file(AllTimePath, AllTimeName)
    elif(time.days >= 365):
        YearlyPath = YearlyPath + str(InYear) + "/Yearly/" + "Andrew's " + str(InYear) + " Financial Report.pdf"
        YearlyName = "Andrew's " + str(InYear) + " Financial Report.pdf"
        if(os.path.exists(YearlyPath)):
            return send_from_directory(YearlyPath, YearlyName)
        else:
            Download_Path, Custom_Name = WebGenerate.WebGen(InitialDate, FinalDate)
            Custom_Name = Custom_Name + '.pdf'
            Download_Path = Download_Path + Custom_Name 
            return send_file(Download_Path, Custom_Name)

    else:
        Download_Path, Custom_Name = WebGenerate.WebGen(InitialDate, FinalDate)
        Custom_Name = Custom_Name + '.pdf'
        Download_Path = Download_Path + Custom_Name 
        return send_file(Download_Path, Custom_Name)


#Show advanced
@app.route("/advanced",methods=['POST', 'GET'])
def advanced():
    cur = Tlbx.dbConnect()
    query = ("Select COUNT(tempID) FROM tTemporary")
    cur.execute(query)
    IncompleteTransaction = cur.fetchone()[0]
    
    #A catch from testing to prevent a crash
    if IncompleteTransaction is None:
        IncompleteTransaction = "0"

    cur = Tlbx.dbConnect()
    query = ("Select COUNT(TransID) FROM tTransaction")
    cur.execute(query)
    CompleteTransaction = cur.fetchone()[0]
    
    #A catch from testing to prevent a crash
    if CompleteTransaction is None:
        CompleteTransaction = "0"    
    return render_template('Advanced/Advanced.html',IncompleteTransaction = IncompleteTransaction, CompleteTransaction = CompleteTransaction)

@app.route("/Advanced/CustomQuery",methods=['POST', 'GET'])
def CustomQuery():
    All = request.form.get('All')
    Specific = request.form['Specific']
    Math = request.form.get('Math')
    Column1 = request.form['Column1']
    Value1 = request.form['Value1']
    Column2 = request.form['Column2']
    Value2 = request.form['Value2']
    
    if (Math != "None" and Math != None):
        Query = "SELECT "
        Query = Query + Math
        if(All == "on"):
            Query = Query + "(*)"
        else:
            Query = Query + "(" + Specific + ")"
        Query = Query + " FROM tTransaction"
        if(Column1 != ""):
            Query = Query + " WHERE " + Column1 + " LIKE '" + Value1 + "'"
            if(Column2 != ""):
                Query = Query + " AND " + Column2 + " LIKE '" + Value2 + "'"
        Query = Query + ";"
        db = pymysql.connect(host='127.0.0.1', port=3306, user='WebServer', password='Momrocks38', db='mydb',autocommit=True)
        cur = db.cursor()
        cur.execute(Query)
        Results = cur.fetchone()[0]
        Results = ('%.2f' % Results)
        return render_template('QueryResults/Math.html', Results = Results)
    else:
        Query = "SELECT TransID, Name, Description, WithdrawDeposit, Company, DATE_FORMAT(Date, '%m-%d-%Y') AS Date, Date AS Sort,  Amount FROM tTransaction"
        if(Column1 != ""):
            Query = Query + " WHERE " + Column1 + " LIKE '" + Value1 + "'"
            if(Column2 != ""):
                Query = Query + " AND " + Column2 + " LIKE '" + Value2 + "'"
        Query = Query + " ORDER BY Sort DESC;"
        cur = Tlbx.dbConnectDict()
        cur.execute(Query)
        return render_template('QueryResults/Many.html', items = cur.fetchall())

#open searchpayment
@app.route("/searchpayment")
def searchpayment():
    return render_template('Search/searchpayment.html', **locals())
    
#finishpayment to edit incomplete transactions
@app.route("/finishpayment")
def finishpayment():
    cur = Tlbx.dbConnectDict()
    query = ("SELECT tempID, WithdrawDeposit, Company, DATE_FORMAT(Date, '%m-%d-%Y') AS Date, Date AS Sort, Amount FROM tTemporary ORDER BY Sort DESC;")
    cur.execute(query)
    return render_template('FinishPayments/finishpaymentSearch.html', items=cur.fetchall())
    
#populating incomplete webpage
@app.route("/finish/<int:tempID>",methods=['POST', 'GET'])
def finish(tempID):
    
    #database connection
    cur = Tlbx.dbConnectDict()
    tempID=str(tempID)
    query = ("SELECT tempID, WithdrawDeposit, Company, DATE_FORMAT(Date, '%m-%d-%Y') AS Date, Amount FROM tTemporary WHERE tempID ="+tempID+";")
    cur.execute(query)
    result=cur.fetchone()
    result=dict(result)
    WithdrawDeposit=result['WithdrawDeposit']
    Company=result['Company']
    Date=(result['Date'])
    Amount=(result['Amount'])
    return render_template('FinishPayments/finish.html',tempID=tempID,WithdrawDeposit=WithdrawDeposit,Company=Company,Date=Date,Amount=Amount)

#Finish incomplete transactions
@app.route("/finishTemp/<int:tempID>",methods=['POST', 'GET'])
def finishTemp(tempID):
    name = ''
    tempID = str(tempID)


    #image orienting and saving
    image = ''
    if request.files['file'].filename != '':
       image = Image.open(request.files['file'].stream)
       if hasattr(image, '_getexif'):
          orientation = 0x0112
          exif = image._getexif()
          if exif is not None:
            orientation = exif[orientation]
            rotations = {
                3: Image.ROTATE_180,
                6: Image.ROTATE_270,
                8: Image.ROTATE_90
            }
            if orientation in rotations:
                image = image.transpose(rotations[orientation])
       name = request.files['file'].filename
       path = '/var/www/Flask/static/' + name
       image.save(path , "JPEG", optimize = True, quality = 85)

    #Get data from web page to upload to database
    Name = request.form['Name']
    Description = request.form['Description']
    WithdrawDeposit = request.form['WithdrawDeposit']
    Company = request.form['Company']
    Date = request.form['Date']
    split = Date.split("-")
    month = split[0]
    day = split[1]
    year = split[2]
    Date = year + "/" + month + "/" + day
    Amount = request.form['Amount']
    Amount = float(Amount)
    Comments = request.form['Comments']
    if (WithdrawDeposit == "Withdraw" and Amount > 0):
        Amount = (Amount * -1)
    request.get_data('Name')
    request.get_data('Description')
    request.get_data('WithdrawDeposit')
    request.get_data('Company')
    request.get_data('Amount')
    request.get_data('Comments')
    cur = Tlbx.dbConnectDict()
    query = (
    "INSERT INTO tTransaction (Name, Description, WithdrawDeposit, Company, Date, Amount, Comments, Receipt) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)")
    data = (Name, Description, WithdrawDeposit, Company, Date, Amount, Comments, name)
    cur.execute(query, data)
    request.get_data('image')
    Date = month + "-" + day + "-" + year
    request.get_data('Date')
    cur = Tlbx.dbConnectDict()
    query = ("DELETE FROM tTemporary WHERE tempID=" + tempID + ";")
    cur.execute(query)
    return render_template("FinishPayments/finishResults.html", Name=Name, Description=Description, WithdrawDeposit=WithdrawDeposit,
                           Company=Company, Date=Date, Amount=Amount, Comments=Comments, image=name)

#Delete Temporary Transactions
@app.route("/DeleteTemp/<int:tempID>",methods=['POST', 'GET'])
def DeleteTemp(tempID):
    tempID = str(tempID)
    query = ("DELETE FROM tTemporary WHERE tempID=" + tempID + ";")
    cur = Tlbx.dbConnectDict()
    cur.execute(query)
    balance = Tlbx.Balance()
    cur = Tlbx.dbConnect()
    query = ("Select COUNT(tempID) FROM tTemporary")
    cur.execute(query)
    Transaction = cur.fetchone()[0]
    if Transaction is None:
        Transaction = "0"
    return render_template('HomePage/index.html', balance = balance, Transaction = Transaction)

#Search page
@app.route("/Paging",methods=['POST', 'GET'])
def Paging():
    Name = request.form['Name']
    Description = request.form['Description']
    WithdrawDeposit = request.form['WithdrawDeposit']
    Company = request.form['Company']
    Date = request.form['Date']
    Amount=request.form['Amount']

    cur = Tlbx.dbConnectDict()

    query = ("SELECT TransID, Name, Description, WithdrawDeposit, Company, DATE_FORMAT(Date, '%m-%d-%Y') AS Date, Date AS Sort,  Amount FROM tTransaction")
    if (Name != '' or Description != '' or WithdrawDeposit != '' or Company != '' or Date != '' or Amount != ''):
        query = query + " WHERE "
        if(Name!= ''):
            query = query + "Name LIKE '"+Name+"'"
            if(Description != '' or WithdrawDeposit != '' or Company != '' or Date != '' or Amount != ''):
                query = query + " AND "
        if(Description!= ''):
            query = query + "Description LIKE '" + Description +"'"
            if(WithdrawDeposit != '' or Company != '' or Date != '' or Amount != ''):
                query = query + " AND "
        if(WithdrawDeposit!= ''):
            query = query + "WithdrawDeposit LIKE '" + WithdrawDeposit + "'"
            if(Company != '' or Date != '' or Amount != ''):
                query = query + " AND "
        if(Company!= ''):
            query = query + "Company LIKE '" + Company +"'"
            if(Date != '' or Amount != ''):
                query = query + " AND "
        if(Date!= ''):
            Date = Date.split("-")
            Month = Date[0]
            Day = Date[1]
            Year = Date[2]
            Date = Year + "-" + Month + "-" + Day
            query = query + "Date LIKE '" + Date + "'"
            if(Amount != ''):
                query = query + " AND "
        if(Amount!= ''):
            query = query + "Amount LIKE " + Amount

    query = query + " ORDER BY Sort DESC;"

    cur.execute(query)
    return render_template('Search/Search.html',items=cur.fetchall())

#Edit complete transactions
@app.route("/approve/<int:TransID>",methods=['POST', 'GET'])
def approve(TransID):
    cur = Tlbx.dbConnectDict()
    TransID=str(TransID)
    query = ("SELECT TransID, Name, Description, WithdrawDeposit, Company, DATE_FORMAT(Date, '%m-%d-%Y') AS Date, Amount, Comments, Receipt FROM tTransaction WHERE TransID ="+TransID+";")
    cur.execute(query)
    result=cur.fetchone()
    result=dict(result)
    Name=result['Name']
    Description=result['Description']
    WithdrawDeposit=result['WithdrawDeposit']
    Company=result['Company']
    Date=(result['Date'])
    Amount=(result['Amount'])
    Comments=(result['Comments'])
    Receipt=(result['Receipt'])
    return render_template('EditTemplate/Edit.html',TransID=TransID,Name=Name,Description=Description,WithdrawDeposit=WithdrawDeposit,Company=Company,Comments=Comments,Date=Date,Amount=Amount,Receipt=Receipt)

#Delete Complete transactions
@app.route("/Delete/<int:TransID>", methods=['POST', 'GET'])
def Delete(TransID):
    TransID=str(TransID)
    query=("DELETE FROM tTransaction WHERE transID="+TransID+";")
    cur = Tlbx.dbConnectDict()
    cur.execute(query)
    balance = Tlbx.Balance()
    cur = Tlbx.dbConnect()
    query = ("Select COUNT(tempID) FROM tTemporary")
    cur.execute(query)
    Transaction = cur.fetchone()[0]
    if Transaction is None:
        Transaction = "0"
    return render_template('HomePage/index.html', balance = balance, Transaction = Transaction)

#Update complete transactions
@app.route("/Update/<int:TransID>", methods=['POST', 'GET'])
def Update(TransID):
    name = ''
    Name = request.form['Name']
    Description = request.form['Description']
    WithdrawDeposit = request.form['WithdrawDeposit']
    Company = request.form['Company']
    Date = request.form['Date']
    split = Date.split("-")
    month = split[0]
    day = split[1]
    year = split[2]
    Date = year + "-" + month + "-" + day
    Amount = request.form['Amount']
    Amount = float(Amount)
    Comments = request.form['Comments']
    name=request.form['Image']
    if (WithdrawDeposit == "Withdraw" and Amount > 0):
        Amount = (Amount * -1)
    if (WithdrawDeposit == "Deposit" or WithdrawDeposit == "deposit" and Amount < 0):
        Amount = abs(Amount)
    Amount=str(Amount)
    TransID=str(TransID)
    request.get_data('Name')
    request.get_data('Description')
    request.get_data('WithdrawDeposit')
    request.get_data('Company')
    request.get_data('Amount')
    request.get_data('Comments')

    if (request.files['file'].filename == '' and request.form['Image']==''):
        name = ''
    elif(request.form['Image']!='' and request.files['file'].filename == ''):
        name=request.form['Image']
    elif(request.files['file'].filename != '' and request.form['Image']==''):
        name = ''
        if request.files['file'].filename != '':
            image = Image.open(request.files['file'].stream)
            if hasattr(image, '_getexif'):
                orientation = 0x0112
                exif = image._getexif()
                if exif is not None:
                    orientation = exif[orientation]
                    rotations = {
                        3: Image.ROTATE_180,
                        6: Image.ROTATE_270,
                        8: Image.ROTATE_90
                    }
                    if orientation in rotations:
                        image = image.transpose(rotations[orientation])
            name = request.files['file'].filename
            path = '/var/www/Flask/static/' + name
            image.save(path, "JPEG", optimize=True, quality=85)
    else:
        if request.files['file'].filename != '':
            name = ''
            if request.files['file'].filename != '':
                image = Image.open(request.files['file'].stream)
                if hasattr(image, '_getexif'):
                    orientation = 0x0112
                    exif = image._getexif()
                    if exif is not None:
                        orientation = exif[orientation]
                        rotations = {
                            3: Image.ROTATE_180,
                            6: Image.ROTATE_270,
                            8: Image.ROTATE_90
                        }
                        if orientation in rotations:
                            image = image.transpose(rotations[orientation])
                name = request.files['file'].filename
                path = '/var/www/Flask/static/' + name
                image.save(path, "JPEG", optimize=True, quality=85)

    cur = Tlbx.dbConnectDict()
    sql = "UPDATE tTransaction SET Name = (%s),Description= (%s),WithdrawDeposit= (%s), Company= (%s), Date=(%s), Amount= (%s), Comments=(%s), Receipt=(%s) WHERE TransID=(%s)"
    cur.execute(sql,(Name,Description,WithdrawDeposit,Company,Date,Amount,Comments,name,TransID))
    Date = month + "-" + day + "-" + year
    request.get_data('Date')
    return render_template("UpdatePayment/Update.html",Name=Name,Description=Description,WithdrawDeposit=WithdrawDeposit,Company=Company,Date=Date,Amount=Amount,Comments=Comments,image=name)

@app.route("/Admin/Console", methods=['POST', 'GET'])
def AdminConsole():
    global s
    global isConnected
    HOST = '192.168.0.20'  # The server's hostname or IP address
    PORT = 8008        # The port used by the server
    try:
        print("Connecting to TwistedServer")
        s.connect((HOST, PORT))
    except:
        return render_template("/Admin/ConsoleFailed.html")
    print("Connected")
    isConnected = True
    return render_template("/Admin/Console.html", async_mode=socketio.async_mode)

def background_thread():
    print("Background Thread Starting")
    global _Machine
    global _CPU
    global _RAM
    global _Uptime
    global _PlexState
    global _MinecraftState
    global _TVShowState
    global _MovieState
    global s
    global isConnected
    while True:
        print('While True')
        if isConnected is not False:
            print("IsConnected Is Not False")
            try:
                print("Receiving Data")
                data = s.recv(1024)
                DataParser(data)
            except:
                print("No Data Yet")
                isConnected = False
            print(data)
        if _Machine == 'Plex-Server':
            #This is to send Plex-Servers CPU/RAM/Uptime to the web page.
            if _CPU and _RAM and _Uptime is not None:
                try:
                    socketio.emit('PlexData',
                    {'CPU': _CPU, 'RAM': _RAM, 'Uptime': _Uptime, 'PlexState': _PlexState, 'MinecraftState': _MinecraftState}, namespace='/Admin/Console')
                except:
                    print("Plex Emit Failed")
        if _Machine == 'Larrys-PC':
            #This is to send Plex-Servers CPU/RAM/Uptime to the web page.
            if _CPU and _RAM and _Uptime is not None:
                try:

                    socketio.emit('PCData',
                    {'CPU': _CPU, 'RAM': _RAM, 'Uptime': _Uptime, 'TVShowState': _TVShowState, 'MovieState': _MovieState}, namespace='/Admin/Console')
                except:
                    print("Larrys-PC Emit Failed")
        if _Machine == 'raspberrypi':
            #This is to send Plex-Servers CPU/RAM/Uptime to the web page.
            if _CPU and _RAM and _Uptime is not None:
                try:
                    socketio.emit('PIData',
                    {'CPU': _CPU, 'RAM': _RAM, 'Uptime': _Uptime}, namespace='/Admin/Console')
                except:
                    print("PI Emit Failed")
        if _Machine == 'Compute-Stick':
            if _CPU and _RAM and _Uptime is not None:
                try:
                    socketio.emit('ComputeData',
                    {'CPU': _CPU, 'RAM': _RAM, 'Uptime': _Uptime}, namespace='/Admin/Console')
                except:
                    print("Compute Emit Failed")
        time.sleep(2)

def DataParser(data):
    print("Parsing ALL THE Data")
    #This is for parsing CPU/RAM data coming in from TwistedServer, and pushing through SocketIO
    global _Machine
    global _CPU
    global _Uptime
    global _RAM
    global _PlexState
    global _MinecraftState
    global _TVShowState
    global _MovieState
    if "Start" not in data and "Stop" not in data and "Restart" not in data and "Shutdown" not in data:
        data = data.split(',')
        _Machine = data[0]
        _CPU = data[1]
        _Uptime = data[2]
        _RAM=data[3]
        if _Machine == "Plex-Server":
            try:
                _PlexState = data[4]
                _MinecraftState = data[5]
            except:
                print("Could Not Get Software States")
        if _Machine == "Larrys-PC":
            try:
                print(_Machine)
                print(_CPU)
                print(_RAM)
                _MovieState = data[4]
                print(_TVShowState)
                _TVShowState = data[5]
                print(_MovieState)
            except:
                print("Could Not Get Software States")

@socketio.on('Commands', namespace='/Admin/Console')
#This collects the Commands sent from the socket on the web page.
def Commands(message):
    #This is for Parsing the command coming from the web page. 
    _Machine = None
    _Command = None
    global s
    print(message['data'])
    message = message['data']
    if message is not None:
        if "Plex-Server" in message:
            print("PlexServer")
            _Machine = "Plex-Server "
        if "Larrys-PC" in message:
            print("Larrys-PC")
            _Machine = "Larrys-PC "
        if "Compute-Stick" in message:
            print("Compute-Stick")
            _Machine = "Compute-Stick "
        if "raspberrypi" in message:
            print("raspberrypi")
            _Machine = "raspberrypi "
        if "Start Plex" in message:
            _Command = "Start Plex"    
        if "Restart Plex" in message:
            _Command = "Restart Plex"
        if "Stop Plex" in message:
            _Command = "Stop Plex"
        if "Start Minecraft" in message:
            _Command = "Start Minecraft"    
        if "Restart Minecraft" in message:
            _Command = "Restart Minecraft"
        if "Stop Minecraft" in message:
            _Command = "Stop Minecraft"
        if "Start conv2mp4-TVShow" in message:
            _Command = "Start conv2mp4-TVShow"    
        if "Restart conv2mp4-TVShow" in message:
            _Command = "Restart conv2mp4-TVShow"
        if "Stop conv2mp4-TVShow" in message:
            _Command = "Stop conv2mp4-TVShow"
        if "Start conv2mp4-Movie" in message:
            _Command = "Start conv2mp4-Movie"    
        if "Restart conv2mp4-Movie" in message:
            _Command = "Restart conv2mp4-Movie"
        if "Stop conv2mp4-Movie" in message:
            _Command = "Stop conv2mp4-Movie"
        if "Restart Machine" in message:
            print('Restart Machine')
            _Command = "Restart Machine"
        if "Shutdown Machine" in message:
            _Command = "Shutdown Machine"
        try:
           Response = "Command " + _Machine + _Command
        except:
            print("Malformed Message")
        try:
            s.sendall(Response)
            print("Sent!")
        except:
            print("Couldn't send")


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    print("Broadcast Message")
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)

@socketio.on('my_ping', namespace='/Admin/Console')
def ping_pong():
    print("My Ping")
    emit('my_pong')
@socketio.on('connect', namespace='/Admin/Console')
def test_connect():
    print("Client Connected")
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
@socketio.on('disconnect', namespace='/Admin/Console')
def test_disconnect():
    print('Client disconnected', request.sid)
'''
def TwistedClient():
    class EchoClientProtocol(Protocol):
        def dataReceived(self, data):
            DataParser(data)
        def callback(self):
            global _Machine
            global _Command
            if _Machine is not None and _Command is not None:
                self.transport.write(_Machine.encode()) 
                _Machine = None
                self.transport.write(_Command.encode())   
                _Command = None   

'''

#Run
if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)
