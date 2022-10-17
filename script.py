from pymongo import MongoClient
import os
import csv
import sys
import smtplib
from email.message import EmailMessage
from datetime import datetime


fields = []
rows = []
tempthreshold=0
tempemail = ''
tempslack = ''
temppagerduty = ''
tempjira = ''
tempquery = ''

def runBQ(query):
    os.system('bq query --nouse_legacy_sql --format=csv "' + query
              + '" > temp.csv')
    parseCSV()

def parseCSV():
    with open('/Users/mminhajuddin/hackathon/temp.csv'
              , 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)
        for i in rows:
            if (tempthreshold > i[1]):
                triggerAlert(i)

        

    csvfile.close()
#------------------Alert-------------------
def triggerAlert(i):
    if tempemail != '':
        msg = EmailMessage()

        # message="Hello Team, Below alert is triggered. Please check accordingly\n"+str(i)+"\nAdding query for reference\n" + str(tempquery)

        cdatetime = datetime.now()
        message = \
            '''From: SRE team


Hello Team, Below alert is triggered at ''' \
            + str(cdatetime) + '. Please check accordingly\n' + str(i) \
            + '''

Adding query for reference
''' + str(tempquery)
        msg.set_content(message)
        msg['Subject'] = 'Alert trigerred'
        msg['From'] = 'pgadhiya@reputation.com'
        msg['To'] = tempemail

        # Send the message via our own SMTP server.

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('pgadhiya@reputation.com', 'HelloJumpCloud#1')
        server.send_message(msg)
        server.quit()

#-----------------------

client = MongoClient()

mydatabase = client.alerts
alerts = mydatabase.alerts


id = sys.argv[1]
cursor = mydatabase.alerts.find({"id" :id })
for i in cursor:
    tempthreshold = 0
    tempemail = ''
    tempslack = ''
    temppagerduty = ''
    tempjira = ''
    if(id == i['id']):
        if(i['source']=='bq'):
            tempthreshold = i['threshold']
            if i['email'] != 'null':
                tempemail = i['email']
            if i['slack'] != 'null':
                tempslack = i['slack']
            if i['jira'] != 'null':
                tempjira = i['jira']
            if i['pagerduty'] != 'null':
                temppagerduty = i['pagerduty']
            tempquery = i['query']
            runBQ(i['query'])
            break
        #elif(i['source']=='Sumo'):
            #runSumo(i[Query])
    else : 
        print("No record found")
