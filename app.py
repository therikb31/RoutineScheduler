from flask import Flask, render_template, request
from flask.json import jsonify
from werkzeug.utils import redirect
from googleapiclient.discovery import build
from google.auth import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import id_token
from google.auth.transport import requests
import pickle
import time
import datetime

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/scheduler")
def scheduler():
    return render_template("dynamicTable.html")


@app.route('/events', methods=['POST'])
def events():
    data = request.get_json()
    print(data)
    scopes = ['https://www.googleapis.com/auth/calendar.events']
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", scopes=scopes)
    credentials = flow.run_console()
    pickle.dump(credentials, open("token.pkl", "wb"))
    credentials = pickle.load(open("token.pkl", "rb"))

    service = build("calendar", "v3", credentials=credentials)
    for i in range(len(data)):
        addevent(data[i],service)
    return redirect("index.html")


def addevent(event,service):
    

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
    '''desc = {
        'summary': title,
        'description': link,
        'start': {
            'dateTime': str(date)+"T"+startTime,
            'timeZone': time.tzname,
        },
        'end': {
            'dateTime': str(date)+"T"+endTime,
            'timeZone': time.tzname,
        },
        'recurrence': [
            'RRULE:FREQ=WEEKLY;COUNT=30'
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 5},
            ],
        },
    }'''
    desc = {
        'summary': title,
        'description': link,
        'start': {
            'dateTime': startDateTime,
            'timeZone': time.tzname,
        },
        'end': {
            'dateTime': endDateTime,
            'timeZone': time.tzname,
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


if __name__ == "__main__":
    app.run(debug=True, port="8000")
