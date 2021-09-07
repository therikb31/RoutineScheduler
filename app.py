from googleapiclient.discovery import build
from google.auth import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("credentials.json",scopes=scopes)
credentials = flow.run_console()

pickle.dump(credentials,open("token.pkl","wb"))
credentials = pickle.load(open("token.pkl","rb"))

service = build("calendar","v3",credentials=credentials)

result = service.events().list(calendarId='primary').execute()
print(result['items'][0])