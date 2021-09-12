from flask import Flask, render_template, request
from flask.json import jsonify
from werkzeug.utils import redirect
from googleapiclient.discovery import build
from google.auth import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import id_token
from google.auth.transport import requests
from pprint import pprint
from Google import Create_Service
import json
import pickle
import time
import datetime

app = Flask(__name__)
CLIENT_SECRET_FILE = 'static/credentials/credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/scheduler")
def scheduler():
    records = open('static/database/records', 'rb')
    records_list = pickle.load(records)
    filename=records_list[-1]+1
    print(records_list,"\n", filename)
    records.close()
    return render_template("dynamicTable.html",filename=filename)


@app.route('/events', methods=['GET','POST'])
def events():
    data = request.get_json()
    records = open('static/database/records', 'rb')
    records_list = pickle.load(records)
    records_list.append(records_list[-1]+1)
    filename = str(records_list[-1])
    export = 'static/database/'+str(filename)
    outfile = open(export, 'wb')
    pickle.dump(data, outfile)
    records.close()
    records = open('static/database/records', 'wb')
    pickle.dump(records_list, records)
    records.close()
    outfile.close()
    print(data)
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    for i in range(len(data)):
        addevent(data[i], service)
    return ("modal.html")

@app.route('/modal', methods=['GET','POST'])
def modal(filename):
    return render_template("modal.html",value=filename)

@app.route('/import', methods=['GET','POST'])
def importSchedule():
    x=0
    return render_template("index.html")

def addevent(event, service):

    title = event['title']
    link = event['link']
    day = event['day']
    startTime = event['from']
    endTime = event['to']
    today = datetime.date.today()
    if(day == "Monday"):
        date = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    elif(day == "Tuesday"):
        date = today + datetime.timedelta(days=1-today.weekday(), weeks=1)
    elif(day == "Wednesday"):
        date = today + datetime.timedelta(days=2-today.weekday(), weeks=1)
    elif(day == "Thursday"):
        date = today + datetime.timedelta(days=3-today.weekday(), weeks=1)
    elif(day == "Friday"):
        date = today + datetime.timedelta(days=4-today.weekday(), weeks=1)
    startDateTime = str(date)+"T"+startTime+":00"
    endDateTime = str(date)+"T"+endTime+":00"
    desc = {
        'summary': title,
        'description': link,
        'start': {
            'dateTime': startDateTime,
            'timeZone': 'IST',
        },
        'end': {
            'dateTime': endDateTime,
            'timeZone': 'IST',
        },
        'recurrence': [
            'RRULE:FREQ=WEEKLY;COUNT=24'
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 5},
            ],
        },
    }
    result = service.events().insert(calendarId='primary', body=desc).execute()


@app.route('/schedule')
def schedular():
    records_list=[100001]
    records = open('static/database/records', 'wb')
    pickle.dump(records_list, records)
    records.close()
    print(records_list)
    return("Ok")


if __name__ == "__main__":
    app.run(debug=True, port="8000")
