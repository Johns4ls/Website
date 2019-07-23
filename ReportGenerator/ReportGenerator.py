import pymysql
from jinja2 import Template
import os
import time
from PIL import Image
import base64
from weasyprint import HTML
from multiprocessing import Process
import time
from datetime import timedelta
import datetime
from datetime import date
import smtplib
import sys
sys.path.append("/var/www/Flask")
from Modules import Tlbx

data= '''
  <!doctype html>
  <link rel="stylesheet" href="C:/Users/johns/Google Drive/ProgrammingProjects/Python/Flask/ReportGenerator/style.css">
  <h1>{{Introduction}}</h1><p>Generated on {{DATE}}.</p>
  <img id=herc src="data:image/jpeg;base64, {{HercPath}}">
  <table>
      <tr>
        <td><h2>Name</h2></td>
        <td><h2>Description</h2></td>
      <td><h2>Type</h2></td>
        <td><h2>Company</h2></td>
        <td><h2>Date</h2></td>
        <td><h2>Amount</h2></td>
        <td><h2>Receipt</h2></td>
      </tr>
  {% for item in items %}
    <p>
    <tr>
      <td><h3>{{item.Name}}</h3></td>
      <td><h3>{{item.Description}}</h3></td>
      <td><h3>{{item.WithdrawDeposit}}</h3></td>
      <td><h3>{{item.Company}}</h3></td>
      <td><h3>{{item.Date}}</h3></td>
      <td><h3>{{item.Amount}}</h3></td>
      <td><img id="image" src="data:image/jpeg;base64, {{item.Receipt}}"></td>
    </tr>
    </p>
  {% endfor %}
  </table>
  </html>'''
t = Template(data)
base_Path='/var/www/Flask/ReportGenerator/'
html_Path=base_Path + 'Temp/'
css_Path="/var/www/Flask/ReportGenerator/style.css"
DATE = time.strftime('%m_%d_%Y')
YEAR = time.strftime('%Y')
baseQuery = "SELECT Name, Description, WithdrawDeposit, Company, DATE_FORMAT(Date, '%m-%d-%Y') AS Date, Date AS Sort, Amount, Receipt FROM tTransaction"
Sort = " ORDER BY Sort DESC;"
currentDate = date.fromtimestamp(time.time())
Math = datetime.timedelta(7)
WeekAgo = currentDate - Math
WeekAgo = str(WeekAgo) 
currentDate=str(currentDate)

def AllTime():
  print("Starting All-Time Report")
  Introduction = "Andrew's Complete Financial Report"
  AllTime_Path = base_Path + 'Reports/All-Time/'
  AllTime_Name = "Andrews Complete Financial Report"
  cur = Tlbx.dbConnectDict()
  query = ( baseQuery + Sort)
  cur.execute(query)
  print("Converting Images")
  items = cur.fetchall()
  items = Tlbx.imgToPNG(items)
  HercPath = Tlbx.HercToPNG()
  print("Rendering HTML")
  Tlbx.RenderHTML(html_Path, t, DATE, items, AllTime_Name, Introduction, HercPath)
  print("Converting to PDF")
  Tlbx.FileRemove(AllTime_Path, AllTime_Name)
  Tlbx.PDFGEN(css_Path, html_Path, AllTime_Path,AllTime_Name)
  print("File successfully created.")

def Yearly():
  print("Starting Yearly Report")
  Introduction = "Andrew's " + YEAR + " Financial Report"
  Yearly_Path = base_Path + 'Reports/' + YEAR + '/Yearly/' 
  Yearly_Name = "Andrew's " + YEAR + " Financial Report"
  cur = Tlbx.dbConnectDict()
  query = (baseQuery + " WHERE YEAR(Date) = " + YEAR + Sort)
  cur.execute(query)
  print("Converting Images")
  items = cur.fetchall()
  items = Tlbx.imgToPNG(items)
  HercPath = Tlbx.HercToPNG()
  print("Rendering HTML")
  Tlbx.RenderHTML(html_Path, t, DATE,items, Yearly_Name, Introduction, HercPath)
  print("Converting to PDF")
  Tlbx.FileRemove(Yearly_Path, Yearly_Name)
  Tlbx.PDFGEN(css_Path, html_Path, Yearly_Path,Yearly_Name)
  print("File successfully created.")
def Monthly():
  print("Starting Monthly Report")
  numberMonth = time.strftime('%m')
  MONTH = Tlbx.convertMonth(numberMonth)
  Introduction = "Andrew's " + MONTH + " " + YEAR + " Financial Report"
  Monthly_Path = base_Path + 'Reports/' + YEAR + '/Monthly/' + MONTH + '/'
  Monthly_Name = "Andrew's " + MONTH + ' ' + YEAR + " Financial Report"
  cur = Tlbx.dbConnectDict()
  query = (baseQuery + " WHERE MONTH(Date) = " + str(numberMonth) +" AND YEAR(Date) = " + str(YEAR) + Sort)
  cur.execute(query)
  print("Converting Images")
  items = cur.fetchall()
  items = Tlbx.imgToPNG(items)
  HercPath = Tlbx.HercToPNG()
  print("Rendering HTML")
  Tlbx.RenderHTML(html_Path, t, DATE,items, Monthly_Name, Introduction, HercPath)
  print("Converting to PDF")
  Tlbx.FileRemove(Monthly_Path, Monthly_Name)
  Tlbx.PDFGEN(css_Path, html_Path, Monthly_Path,Monthly_Name)
  print("File successfully created.")
def Weekly():
    print("Starting Weekly Report")
    Introduction = "Andrews Financial Report for the week of " + currentDate 
    Weekly_Path = base_Path + 'Reports/'+ YEAR + '/' + 'Weekly/' + currentDate + '/'
    Weekly_Name = "Andrew's Financial Report " + currentDate
    cur = Tlbx.dbConnectDict()
    query = (baseQuery + " WHERE Date BETWEEN '" + str(WeekAgo) + "' and '" + str(currentDate) + "'" + Sort)
    cur.execute(query)
    print("Converting Images")
    items = cur.fetchall()
    items = Tlbx.imgToPNG(items)
    HercPath = Tlbx.HercToPNG()
    print("Rendering HTML")
    try:
      Tlbx.RenderHTML(html_Path, t, DATE,items, Weekly_Name, Introduction, HercPath)
      print("Converting to PDF")
      Tlbx.FileRemove(Weekly_Path, Weekly_Name)
      Tlbx.PDFGEN(css_Path, html_Path, Weekly_Path,Weekly_Name)
      print("File successfully created.")
    except:
      print("No Transactions")


if __name__ == '__main__':
  class CreatePDFs():
    try:
      Report_AllTime = Process(target = AllTime)
      Report_Yearly = Process(target = Yearly)
      Report_Monthly = Process(target = Monthly)
      Report_Weekly = Process(target = Weekly)
      Report_AllTime.start()
      Report_Yearly.start()
      Report_Monthly.start()
      Report_Weekly.start()
      Report_AllTime.join()
      Report_Yearly.join()
      Report_Monthly.join()
      Report_Weekly.join()
    except:
      print("Report Generation Failed! Sending Email...")
      body = "Report Generation Failed"
      Tlbx.SendEmail(body)
