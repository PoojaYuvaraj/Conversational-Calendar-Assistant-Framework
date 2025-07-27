import os
import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_calendar_service():
    creds_path = os.getenv("GOOGLE_CLIENT_SECRET_PATH")
    scopes = ['https://www.googleapis.com/auth/calendar']
    credentials = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
    return build('calendar', 'v3', credentials=credentials)

def create_meeting(event_info: dict):
    service = get_calendar_service()
    timezone = 'America/Chicago'  # or change to your preferred

    start_dt = datetime.datetime.strptime(f"{event_info['date']} {event_info['time']}", "%Y-%m-%d %H:%M")
    end_dt = start_dt + datetime.timedelta(minutes=event_info["duration"])

    event = {
    'summary': event_info["title"],
    'start': {'dateTime': start_dt.isoformat(), 'timeZone': timezone},
    'end': {'dateTime': end_dt.isoformat(), 'timeZone': timezone},
    # No attendees
    }

    return service.events().insert(calendarId='primary', body=event).execute()
