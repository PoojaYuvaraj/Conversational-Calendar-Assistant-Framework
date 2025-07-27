from google.oauth2 import service_account
from googleapiclient.discovery import build

def setup_shared_calendar(service_account_file: str, share_with_email: str) -> str:
    # Authenticate with service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    service = build('calendar', 'v3', credentials=credentials)

    # 1. Create a new calendar
    calendar = {
        'summary': 'Meeting Scheduler Bot',
        'timeZone': 'America/Chicago'
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    calendar_id = created_calendar['id']
    print(f"✅ Created calendar: {calendar_id}")

    # 2. Share the calendar with your email
    rule = {
        'scope': {
            'type': 'user',
            'value': share_with_email
        },
        'role': 'writer'
    }

    service.acl().insert(calendarId=calendar_id, body=rule).execute()
    print(f"✅ Shared with {share_with_email}")

    return calendar_id

if __name__ == "__main__":
    calendar_id = setup_shared_calendar(
        service_account_file="credentials.json",
        share_with_email="pooja.yuva98@gmail.com"
    )
    print("Use this calendar ID when creating events:", calendar_id)
