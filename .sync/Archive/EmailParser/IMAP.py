import pymysql
import imaplib
import email
import threading
import time
import socket
import re
import base64
from threading import Thread
from HTMLParser import HTMLParser
import smtplib
import sys
sys.path.append("/var/www/Flask/")
from Modules import Tlbx
#Declarations of variables
Amount = ''
to_ = ''
subject = ''
date = ''


def dbTrans(Name, Description, WithdrawDeposit, Company, Date, Amount, Comments, Receipt):
    print("dbTrans works!")
    cur = Tlbx.dbConnect()
    query = "INSERT INTO tTransaction (Name, Description, WithdrawDeposit, Company, Date, Amount, Comments, Receipt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    print(Date)
    data = (Name, Description, WithdrawDeposit, Company, Date, Amount, Comments, Receipt)
    try:
        cur.execute(query, data)
    except:
        body = "IMAP failed. Name was %s, Description was %s, Subject was %s, Company was %s, Date was %s Amount was %s Comments was %s Receipt was %s", (Name, Description, WithdrawDeposit, Company, Date, Amount, Comments, Receipt)
        Tlbx.SendEmail(body)    

def dbTemp(WithdrawDeposit, Company, Date, Amount):
    print("dbTemp works!")
    query = ("INSERT INTO tTemporary (WithdrawDeposit, Company, Date, Amount) VALUES (%s, %s, %s, %s)")
    data = (WithdrawDeposit, Company, Date, Amount)
    cur = Tlbx.dbConnect()
    try:
        cur.execute(query, data)
    except:
        print("PNC Database insert Failed! Sending email...")
        body = "IMAP failed. Subject was " + WithdrawDeposit + " Company was " + Company + " Date was " + Date + " Amount was " + str(Amount)
        Tlbx.SendEmail(body)


#html parsing class which takes the body data in html and parses the information and appends it to a variable, called later
class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attributes):
        self.inLink = False
        if tag == 'h2':
            self.inLink = True
            self.lasttag = tag
        elif tag =='h4':
            self.inLink = True
            self.lasttag = tag

            def handle_endtag(self, tag):
                if tag == 'h4':
                    self.inlink = False
                elif tag == 'h2':
                    self.inlink = False

    def handle_data(self, data,):
        if self.lasttag == 'h2' and self.inLink and data.strip():
            if data == '\n':
                return
            elif data == '\t':
                return
            elif data == '':
                return
            else:

                body.append(data)

        elif self.lasttag == 'h4' and self.inLink and data.strip():
            if data == '\n':
                return
            elif data == '\t':
                return
            elif data == '':
                return
            else:
                body.append(data)
class MyCheckParser(HTMLParser):

    def handle_starttag(self, tag, attributes):
        self.inLink = False
        if tag =='h4':
            self.inLink = True
            self.lasttag = tag

            def handle_endtag(self, tag):
                if tag == 'h4':
                    self.inlink = False

    def handle_data(self, data,):
        if self.lasttag == 'h4' and self.inLink and data.strip():
            if data == '\n':
                return
            elif data == '\t':
                return
            elif data == '':
                return
            else:
                body.append(data)

#main function of the program. This program takes emails from pncalerts and mobile(credit card alert) and commits
#the data that comes in to the database.
def IMAP():

    #Global variable to use inside of the class above
    global body

    #Connect to gmails imap service 
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('Johnsonandrew123198@gmail.com', 'Momrocks38')
        mail.select('inbox')
        mail.list()
    except:
        print("Could not connect to Gmail!")
        body = "IMAP failed. Could not connect to Gmail."
        Tlbx.SendEmail(body)

    
    #this will search the email and give me all unread emails.
    status, response = mail.search(None, '(UNSEEN)')
    response = response[0].split()
    
    #For each email we will parse out the data and commit to the database
    for e_id in response:
    
        #reset variables for each loop
        body =[]
        raw_email = ''
        
        #Fetch one email and decode as utf-8
        _, response = mail.fetch(e_id, 'RFC822')
        try:
            raw_email = response[0][1].decode("utf-8")
        except:
            print("Email cannot be decoded")
            continue
        email_message = email.message_from_string(raw_email)
        
        #these pull each heading and place into variables
        from_ = email_message['From']
        subject_ = str(email_message['Subject'])
        date_ = str(email_message['date'])
        #set up array for date
        date = []
        try:
            date = date_.split()
            Day = (date[0])
            Month = (date[1])
            Year = (date[2])
            Date = Tlbx.dateConvert(Day, Month, Year)
        except:
            print("Date Failed!")
            body = "IMAP Date parsing failed. %s was the date pulled in" % date_
            Tlbx.SendEmail(body)

        #If this data from pncalerts, we run it through this parsing group
        if (from_ == "PNC Alerts <pncalerts@pnc.com>"):
            if( "ATM" in subject_):
                print("There should be no ATM usage!")
                body = "Someone pulled money out of the ATM using Andrew's card."
                Tlbx.SendEmail(body)
                continue
            elif( "Your Checking Account Balance" in subject_):
                parser = MyCheckParser()
                parser.feed(str(email_message))
                PNCBalance = body[0]
                PNCBalance = PNCBalance.split(":")
                PNCBalance = PNCBalance[1]
                PNCBalance = PNCBalance.replace("$", "")
                PNCBalance = PNCBalance.replace(",", "")
                PNCBalance = PNCBalance.strip()
                PNCBalance=float(PNCBalance)
                db = pymysql.connect(host='192.168.0.20', port=3306, user='Test', password='Momrocks38', db='mydb',autocommit=True)
                cur = db.cursor()
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
                balance=float(balance)
                if(balance != PNCBalance):
                    PNCBalance = str(PNCBalance)
                    balance = str(balance)
                    print("Balances do not match!")
                    body = "PNC and app balances do not match. PNC balance is " + PNCBalance + " and app balance is " + balance + "."
                    Tlbx.SendEmail(body)

            elif( "Check(s)" in subject_):
                parser = MyCheckParser()
                parser.feed(str(email_message))
                if( "Deducted" in subject_):
                    WithdrawDeposit = "Withdraw"
                else:
                    WithdrawDeposit = "Deposit"
                #The global variable body we now get who the money is from and strip excess
                Company = 'Check'
                Amount = body[2]
                Amount = Amount.strip()
                Amount = Amount.split(":")
                Amount = Amount[1]
                Amount = Amount.replace("$", "")
                Amount = Amount.strip()
                #database connector
                Day = date[1]
                Month = date[2]
                Year = date[3]
                Date = Tlbx.dateConvert(Day, Month, Year)
                #Function to connect to database and commit data to tTemporary
                dbTemp(WithdrawDeposit, Company, Date, Amount)       
            else:
                #This sets up our html parser which is the class above and feeds it in.
                parser = MyHTMLParser()
                parser.feed(str(email_message))
                Company = ''
                Amount = ''
                #The global variable body we now get who the money is from and strip excess
                try:
                    Company = body[1]
                    Company = Company.strip('\t')
                    Company = Company.strip('\n')
                    Company = Company.strip()
                    
                    #pull how much the amount was for and strip excess
                    Amount = body[2]
                    Amount = Amount.strip('\t')
                    Amount = Amount.strip('\n')
                    Amount = Amount.strip()
                    Amount = re.findall("\d+\.\d+", Amount)
                except:
                    print("Company and Amount parsing Failed!")
                    body = "IMAP Company/Amount parsing failed. %s was the Company pulled in, and %s was the the Amount pulled in" % (Company, Amount)
                    Tlbx.SendEmail(body)
                    continue
                
                #try to convert Amount for database commit
                try:
                    Amount = Amount[0]
                    Amount = float(Amount)
                except:
                    print("no money I guess")
                    
                
                #Date comes in differently, parse again. Could be avoided with external function
                if ('Payment' in subject_ or 'Withdraw' in subject_):
                    subject_ = 'Withdraw'
                    Day = date[1]
                    Month=date[2]
                    Year=date[3]
                    Date = Tlbx.dateConvert(Day, Month, Year)
                elif ('Available Balance' in subject_):
                    continue
                elif ('Online Banking alerts' in subject_):
                    continue
                else:
                    subject_ = 'Deposit'
                    Day = date[1]
                    Month=date[2]
                    Year = date[3]
                    Date = Tlbx.dateConvert(Day, Month, Year)
                # switch the Amount to negative if it is a withdraw
                if ('Withdraw' in subject_):
                    Amount = -Amount
                    
                #Strip excess data
                Company = Company.replace('Payment', '')
                Company = Company.replace('From:', '')
                Company = Company.replace('1', '')
                Company = Company.replace('To:', '')
                Company = Company.strip()
                
                #Logic to automatically fill out bills and commit directly to tTransaction
                if ("DUKE ENERGY OH" in Company or "RUMPKE RESIDENTI" in Company or "CLERMONT COUNTY" in Company or "SSI  TREAS 30    9" in Company or "US BANK HOME MTG" in Company):
                    Name = ''
                    Description = ''
                    Comments = ''
                    Receipt = ''
                    if ("CLERMONT COUNTY" in Company):
                        Company = "Clermont County Utilities"
                        Description = "Monthly Water Bill Payment"
                        Name = "Clermont County Water"
                    if ("RUMPKE RESIDENTI" in Company):
                        Company = "Rumpke"
                        Description = "Monthly Payment for Waste Disposal"
                        Name = "Trash Removal"
                    if ("DUKE ENERGY OH" in Company):
                        Company = "Duke Energy"
                        Description = "Monthly Electric Bill"
                        Name = "Duke Energy"
                    if ("SSI  TREAS 30    9" in Company):
                        Company = "SSI"
                        Description = "Monthly Social Security Deposit"
                        Name = "SSI Check Deposit"
                    if("US BANK HOME MTG" in Company):
                        Company = "US Bank"
                        Description = "Monthly House Payment"
                        Name = "Housing"
                    #Function to connect to our database and insert into tTransaction
                    dbTrans(Name, Description, subject_, Company, Date, Amount, Comments, Receipt)
                #commit data to our incomplete tTemporary table
                else:
                    #Function to connect to our database and insert into tTemporary
                    dbTemp(subject_, Company, Date, Amount)
                
        #If the email is from mobile@visammg.com it will run through here
        elif(from_=='mobile@visammg.com'):
        
            #Pull email and decode because it is in base64
            ascil = email_message.get_payload(decode=base64).decode("utf-8")
            
            #Here we split the array and place them into variables. From there we strip them down.
            array = (ascil.split("\n", 1))
            startType = 'Your'
            endType = 'specified'
            start = 'Amount:'
            end = 'USD'
            Start1 = 'Name:'
            end1 = 'Merchant'
            start2 = 'Location:'
            end2 = ','
            s = array[1]
            WithdrawDeposit = ((s.split(startType))[1].split(endType)[0])
            if("purchase" in WithdrawDeposit):
                WithdrawDeposit = "Withdraw"
            if("deposit" in WithdrawDeposit):
                WithdrawDeposit = "Deposit"
            if("recently used" in WithdrawDeposit):
                WithdrawDeposit = "Withdraw"
                
            #Setup our amount to commit to the database
            Amount = ''
            try:
                Amount = ((s.split(start))[1].split(end)[0])
                Amount = Amount.strip('\t')
                Amount = Amount.strip('\n')
                Amount = Amount.strip()
                Amount = Amount.replace('\'', '')
                Amount = Amount.replace("'", '')
                Amount=float(Amount)
                if (WithdrawDeposit == "Withdraw"):
                    Amount = Amount * -1
            except:
                print("No Amount I Guess")
                
            #Parse down the company
            Company = ((s.split(Start1))[1].split(end1)[0])
            Company = Company.strip('\t')
            Company = Company.strip('\n')
            Company = Company.strip()
            
            #if we are one of these, commit directly to tTransaction
            if("ORDER" in Company or "BALANC" in Company or "TIP" in Company or "Northshore Care Supply" in Company ):
                Name = ''
                Description = ''
                Comments = ''
                Receipt = ''
                if("ORDER" in Company):
                    Company = "Shipt"
                    Name    = "Groceries"
                    Description = "Monthly Groceries"
                if("BALANC" in Company):
                    Company = "Shipt"
                    Name = "Groceries"
                    Description = "Balance differential for adding an item"
                if("TIP" in Company):
                    Company = "Shipt"
                    Name = "Groceries"
                    Description = "Added tip for Delivery"
                if("Northshore Care Supply" in Company):
                    Company = "Northshore Care Supply"
                    Name = "Diapers"
                    Description = "Tranquility All Night Through Adult Disposable Briefs"
                    
                #Function call to create database connection and insert data to tTransaction
                dbTrans(Name, Description, WithdrawDeposit, Company, Date, Amount, Comments, Receipt)

            #commit to tTemporary table
            else:
                #Parse company names to make it easier to finish
                if("CW BOTANICALS" in Company or "MEIJER" in Company or "FIVE BELOW" in Company or "LOWE'S" in Company or "KROGER" in Company or "MCDONALD'S" in Company or "WALGREENS" in Company or "AMZN MKTP US AMZN.COM/" in Company or "AMAZON" in Company or "AMZN Mktp" in Company or "Amazon" in Company or "amazon" in Company or "THORNTONS" in Company or "KFC" in Company or "TARGET" in Company):
                    if("CW BOTANICALS" in Company):
                        Company = "CW Botanicals"
                    if("MEIJER" in Company):
                        Company = "Meijer"                   
                    if("FIVE BELOW" in Company):
                        Company = "Five Below"
                    if("LOWE'S" in Company):
                        Company = "Lowe's"
                    if("KROGER" in Company):
                        Company = "Kroger"
                    if("WALGREENS" in Company):
                        Company = "Walgreens"
                    if("AMAZON" in Company or "AMZN MKTP US AMZN.COM/" in Company or "Amazon" in Company or "amazon" in Company):
                        Company = "Amazon"
                    if("THORNTONS" in Company):
                        Company = "Thorntons"
                    if("KFC" in Company):
                        Company = "KFC"
                    if("TARGET" in Company):
                        Company = "Target"
                #Function call to create database connection and insert data to tTemporary
                dbTemp(WithdrawDeposit, Company, Date, Amount)
#Here is our main class that starts our function.
class EmailParser():

    t1 = threading.Thread(name='IMAP', target=IMAP())
    t1.start()
