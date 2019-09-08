#Various imports
from flask import Flask, flash, render_template, send_from_directory, request, redirect, url_for, send_file, session
import pymysql
from werkzeug.utils import secure_filename
import os
import PIL
from PIL import Image, ExifTags
from datetime import date, datetime, timedelta
import sys
import time
from Modules import Tlbx
import math
import sys
import time
from os import listdir
from os.path import isfile, join

#Set upload folder for receipt images, and set max upload size
Base_Path = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = Base_Path + '/static/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.secret_key = 'some_secret'


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

#Run
if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)
