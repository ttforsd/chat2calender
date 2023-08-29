from __future__ import print_function

import datetime
import os.path
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



load_dotenv()
calendar_id = os.getenv('CALENDAR_ID')

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


def gcal_main(event, me = True):
    event = parse_event(event, me)
    return write2gcal(event)



def write2gcal(event_dict):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        event = service.events().insert(calendarId=calendar_id, body=event_dict).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        dt = event.get('start').get('dateTime')
        if dt != None: 
            dt = datetime.datetime.fromisoformat(dt)
            dt = dt.strftime("%A %d/%m/%Y %H:%M")
        else: 
            dt = event.get('start').get('date')
            dt = datetime.datetime.fromisoformat(dt)
            dt = dt.strftime("%A %d/%m/%Y")
        return f"Event: {event.get('summary')} on {dt}. Link: {event.get('htmlLink')}"

    except HttpError as error:
        print('An error occurred: %s' % error)


event = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'start': {
    'dateTime': '2023-08-22T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2023-08-22T17:00:00-13:00',
    'timeZone': 'America/Los_Angeles',
  }
}



def parse_event(event, nothk=True): 
    """Parses json to correct format"""
    event_dict = {}
    event_dict['summary'] = event["Event_Name"]
    start, end = start_end_time(event["Event_Date"], event["Event_Time"])
    if nothk: 
        start["start"]["timeZone"] = "Europe/London"
        end["end"]["timeZone"] = "Europe/London"
    else:
        start["start"]["timeZone"] = "Asia/Hong_Kong"
        end["end"]["timeZone"] = "Asia/Hong_Kong"
    event_dict.update(start)
    event_dict.update(end)
    event_dict['description'] = {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 12 * 60},
        {'method': 'popup', 'minutes': 45},
        ]}
    print(start, end)
    return event_dict

def start_end_time(date,time): 
    # return endtime = starttime + 1 hour, return list of dictionary of start and end time
    all_day = time == "00:00"
    start = parse_datetime(date, time)
    # convert start to datetime object
    start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
    end = start + datetime.timedelta(hours=1)
    start = start.isoformat()
    end = end.isoformat()
    if not all_day:
        start = {'start': {'dateTime': start}}
        end = {'end': {'dateTime': end}}
    else: 
        start = {'start': {'date': start[:10]}}
        end = {'end': {'date': end[:10]}}
    return [start, end]

def parse_datetime(date, time): 
    """Parses date and time to correct format"""
    after = isafter(date)
    if after: 
        year = datetime.datetime.now().year
    else:
        year = datetime.datetime.now().year + 1
    date = date.split("/")
    time = time.split(":")
    month = int(date[1])
    day = int(date[0])
    hour = int(time[0])
    minute = int(time[1])
    return datetime.datetime(year, month, day, hour, minute).isoformat()

def isafter(date): 
    today_month = datetime.datetime.now().month
    today_day = datetime.datetime.now().day
    date = date.split("/")
    month = int(date[1])
    day = int(date[0])
    if month > today_month: 
        return True
    elif month == today_month: 
        if day > today_day: 
            return True
    return False


if __name__ == '__main__':
    main()