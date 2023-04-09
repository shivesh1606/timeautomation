from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
from datetime import *
import pytz
import csv

import pandas as pd
import openpyxl
import os
def deauth():
    try:
        os.remove('token.json')
        print("Token Removed")
    except:
        print("Token Not Found")
    return True
#find token.json file and return credentials
def is_authenticated():
    if os.path.isfile('token.json'):
        return True
    else:
        return False
def get_token():
    if os.path.isfile('token.json'):
        token=open('token.json')
        token=token.read()
        token=token.split('"')
        token=token[3]
        print(token)

        return token
    else:
        return False

def get_user_profile(token):
    url= "https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token="+token
    response=requests.get(url)
    return response.json()
    # if os.path.isfile('token.json'):
    #     #return access token
    #     token = open('token.json')
    #     return token['to']
    # else:
    #     return False

def get_events(service):
    # Call the Calendar API    
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events=service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
    return events.get('items', [])


def get_events_by_date(api_service, event_date):

    split_date = event_date.split('-')

    event_date = datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]), 00, 00, 00, 0)
    # event_date = pytz.UTC.localize(event_date).isoformat()
    event_date=datetime.strftime(event_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    end = datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]), 23, 59, 59, 999999)
    end=datetime.strftime(end, '%Y-%m-%dT%H:%M:%S.%fZ')
    print(">>>>>>>>>>> Gettings events for date: ", event_date)
    events_result = api_service.events().list(calendarId='primary', timeMin=event_date,timeMax=end,singleEvents=True,orderBy='startTime').execute()
    return events_result.get('items', [])

def get_events_by_date_range(api_service, start_Date, end_Date):
    start_Date=datetime.strptime(start_Date, '%Y-%m-%d')
    end_Date=datetime.strptime(end_Date, '%Y-%m-%d')
    end_Date=end_Date+timedelta(days=1)
    date_range=[start_Date+timedelta(days=x) for x in range((end_Date-start_Date).days)]
    event_list=[]
    for date in date_range:
        date=date.strftime('%Y-%m-%d')
        events=get_events_by_date(api_service,str(date))
        for event in events:
            event_list.append(event)
    
    return event_list
    # start_split_date = start_Date.split('-')
    # end_split_date = end_Date.split('-')
    # event_start_date = datetime(int(start_split_date[0]), int(start_split_date[1]), int(start_split_date[2]), 00, 00, 00, 0)
    # event_start_date = pytz.UTC.localize(event_start_date).isoformat()

    # event_end_date = datetime(int(end_split_date[0]), int(end_split_date[1]), int(end_split_date[2]), 23, 59, 59, 999999)
    # event_end_date = pytz.UTC.localize(event_end_date).isoformat()
    # print("Start date is  ",event_start_date)
    # print("End date is  ",event_end_date)
    # events_result = api_service.events().list(calendarId='primary', timeMin=event_start_date,timeMax=event_end_date, timeZone="UTC").execute()
    # print(events_result)
    # return events_result.get('items', [])
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/userinfo.profile']

def get_user_info(token):
    url= "https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token="+token
    response=requests.get(url)
    print(response.json())

def auth():
    print("Something")
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
    return creds

def main(query,start_Date=None,end_Date=None):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    print("Going for Credentials")
    creds = auth()
    print(creds)
    print(creds.token)
    print(get_user_info(creds.token))
    service = build('calendar', 'v3', credentials=creds)
    event_dict_list=[]
    list_of_events=[]
    if query==1:
        events=get_events(service)
    elif query==2:
        events=get_events_by_date(service,start_Date)
    elif query==3:
        events=get_events_by_date_range(service,start_Date,end_Date)
    else:
        print("Invalid choice")

    for event in events:
            try:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end=event['end'].get('dateTime', event['end'].get('date'))
                event_start_date = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
                event_start_date=event_start_date.astimezone(pytz.timezone('Asia/Kolkata'))
                event_end_date = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')
                event_end_date=event_end_date.astimezone(pytz.timezone('Asia/Kolkata'))
                event_start_time=event_start_date.strftime("%H:%M:%S")
                event_end_time=event_end_date.strftime("%H:%M:%S")
                event_start_date=event_start_date.strftime("%Y-%m-%d")
                event_end_date=event_end_date.strftime("%Y-%m-%d")
                location=''
                try:
                    location=event['location']
                except Exception as e:
                    pass
                title=event['summary']
                creator=event['creator']['email']
                attendees=[]
                try:
                    for attendee in event['attendees']:
                        attendees.append(attendee['email'])
                except:
                    pass
                event_dict={
                    "title":title,
                    "creator":creator,
                    "attendees":attendees,
                    "start_date":event_start_date,
                    "start_time":event_start_time,
                    "end_date":event_end_date,
                    "end_time":event_end_time,
                    "location":location

                }
                event_list=[title,creator,attendees,event_start_date,event_start_time,event_end_date,event_end_time,location]
                list_of_events.append(event_list)
            except Exception as e:
                print(e)
                pass 
    dict_header = {0:'Title',
    1:'Creator' ,
    2:'Attendees',
    3:'Start Date',
    4:'Start Time',
    5:'End Date',
    6:'End Time',
    7:'Location'}
    df=pd.DataFrame(list_of_events)
    df.rename(columns=dict_header,
    inplace=True)
    BaseDir=os.path.dirname(os.path.abspath(__file__))
    path=os.path.join(BaseDir,"SavedCalendar/")
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(path+"SavedCalendar.csv"):
        os.remove(path+"SavedCalendar.csv")
    print(path+"SavedCalendar.csv")

    filepath=os.path.join(path,"SavedCalendar.csv")
    if query==2:
        filepath=os.path.join(path,"SavedCalendar_"+start_Date+".csv")
    elif query==3:
        filepath=os.path.join(path,"SavedCalendar_"+start_Date+"_"+end_Date+".csv")

    df.to_csv(filepath,index=False)
    if not events:
        print('No upcoming events found.')
        return
if __name__ == '__main__':
    main()