import os
import time
import datetime
import smtplib
# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databses names one on each line and assignd to DB_NAME variable.

DB_HOST = 'localhost'
DB_USER = 'WebServer'
DB_USER_PASSWORD = 'Momrocks38'
DB_NAME = 'mydb'
BACKUP_PATH = '/var/www/Flask/DatabaseBackup/DatabaseBackup/'
try:

    # Getting current datetime to create seprate backup folder like "12_31_1998".
    DATE = time.strftime('%m_%d_%Y')

    TODAYBACKUPPATH = BACKUP_PATH + DATE

    # Checking if backup folder already exists or not. If it doesnt, create it.
    print("Creating Backup Folder")
    if not os.path.exists(TODAYBACKUPPATH):
        os.makedirs(TODAYBACKUPPATH)
        
    # Creating Backup
    print("Creating Backup Script")
    db = DB_NAME
    dumpcmd = "mysqldump -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + TODAYBACKUPPATH + "/" + db + ".sql"
    os.system(dumpcmd)

    print("Backup Script Created")
    print("Your backups has been created in '" + TODAYBACKUPPATH + "' directory")
except:
    print("Database Backup Failed! Sending Email...")
    body = "Database Backup failed."
    SendEmail(body)
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
