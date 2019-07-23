import pymysql
from jinja2 import Template
import os
import time
from PIL import Image
import base64
from weasyprint import HTML
from multiprocessing import Process
import time
from datetime import timedelta, date
import datetime
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
def WebGen(InitialDate, CurrentDate):
    print("Starting Web Generation")
    Introduction = "Andrew's Web-Generated Report between " + InitialDate+" And " + CurrentDate
    Download_Path = base_Path + 'Reports/'+ YEAR + '/' + 'Custom/' + currentDate + '/'
    Custom_Name = "Andrew's Custom Financial Report " + currentDate
    cur = Tlbx.dbConnectDict()
    InitialDate = InitialDate.split('/')
    CurrentDate=CurrentDate.split('/')
    InitialDate = InitialDate[2] + '/' + InitialDate[0] + '/' + InitialDate[1]
    CurrentDate = CurrentDate[2] + '/' + CurrentDate[0] + '/' + CurrentDate[1]
    query = (baseQuery + " WHERE Date BETWEEN '" + str(InitialDate) + "' and '" + str(CurrentDate) + "'" + Sort)
    cur.execute(query)
    print("Converting Images")
    items = cur.fetchall()
    items = Tlbx.imgToPNG(items)
    HercPath = Tlbx.HercToPNG()
    print("Rendering HTML")
    try:
        Tlbx.RenderHTML(html_Path, t, DATE, items, Custom_Name, Introduction, HercPath)
    except:
        print("Html broke")
    try:
        print("Converting to PDF")
        Tlbx.PDFGEN(css_Path, html_Path,Download_Path,Custom_Name)
        print("File successfully created.")
    except:
        "PDF broke"
    try:
        return Download_Path, Custom_Name
    except:
        print("Return broke")