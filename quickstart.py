from googleapiclient.discovery import build
from google.auth import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import time
scopes = ['https://www.googleapis.com/auth/calendar.events']
flow = InstalledAppFlow.from_client_secrets_file("credentials.json",scopes=scopes)
credentials = flow.run_console()

pickle.dump(credentials,open("token.pkl","wb"))
credentials = pickle.load(open("token.pkl","rb"))

service = build("calendar","v3",credentials=credentials)

event = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2021-09-09T09:00:00',
    'timeZone': time.tzname,
  },
  'end': {
    'dateTime': '2021-09-09T17:00:00',
    'timeZone': time.tzname,
  },
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
result = service.events().insert(calendarId='primary',body=event).execute()
print ('Event created:')
#print(result['items'][0])