from tkinter import E
from unicodedata import name
from flask import *  
import os
import random
import string
from pymongo import MongoClient
from crontab import CronTab

app = Flask(__name__)  
app.secret_key = "super secret key"

client = MongoClient('localhost', 27017)
	
my_cron = CronTab(user='mminhajuddin')
db = client.alerts
alerts = db.alerts
count = alerts.count_documents({})
# A decorator used to tell the application
# which URL is associated function
@app.route('/' '/index.html', methods =["GET", "POST"])
def index():
    data = alerts.find() 
    return render_template('index.html' , data=data, count=count)

       #return "fname"
    #return render_template("home.html")
 
@app.route('/sumologic-input.html')
def sumo_input():
    if request.method == "POST":
       if request.method=='POST':
            id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            source = 'bq'
            dept = request.form['dept']
            query = request.form['query']
            description  = request.form['description']
            threshold = request.form['threshold']
            freq = request.form['freq']
            slack = request.form['slack'] or None
            email = request.form['email'] or None
            jira = request.form['jira'] or None 
            pagerduty = request.form['pagerduty'] or None
            password = request.form['password']
            print(dept,query,description,threshold,freq,slack,email,jira,pagerduty,password)
            alerts.insert_one({'id':id,'source': source, 'dept': dept, 'query': query, 'description': description, 'threshold': threshold, 'freq': freq, 'email': email, 'slack': slack, 'jira': jira, 'pagerduty': pagerduty, 'password': password})
            flash('You were successfully logged in')
            return redirect(url_for('index'))

    return render_template('sumologic-input.html')

@app.route('/bq-input.html', methods =["GET", "POST"])
def bq_input():
    if request.method == "POST":
       if request.method=='POST':
            id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            source = 'sumologic'
            dept = request.form['dept']
            query = request.form['query']
            description  = request.form['description']
            threshold = request.form['threshold']
            freq = request.form['freq']
            slack = request.form['slack'] or None
            email = request.form['email'] or None
            jira = request.form['jira'] or None
            pagerduty = request.form['pagerduty'] or None
            password = request.form['password']
            print(dept,query,description,threshold,freq,slack,email,jira,pagerduty,password)
            alerts.insert_one({'id':id,'source': source, 'dept': dept, 'query': query, 'description': description, 'threshold': threshold, 'freq': freq, 'email': email, 'slack': slack, 'jira': jira, 'pagerduty': pagerduty, 'password': password})
            job = my_cron.new(command='python /Users/mminhajuddin/hackathon/script.py'+' '+ id)
            if (freq == 'weekly'):
                job.day.every(7)
            else :
                job.hour.every(freq)
            my_cron.write()
            flash('You were successfully logged in')
            return redirect(url_for('index'))

    return render_template('bq-input.html') 

if __name__=='__main__':
   app.run(host='0.0.0.0', port=80, debug="true")