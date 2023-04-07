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
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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
    event_date = pytz.UTC.localize(event_date).isoformat()

    end = datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]), 23, 59, 59, 999999)
    end = pytz.UTC.localize(end).isoformat()

    events_result = api_service.events().list(calendarId='primary', timeMin=event_date,timeMax=end, timeZone="UTC").execute()
    return events_result.get('items', [])

def get_events_by_date_range(api_service, start_Date, end_Date):

    start_split_date = start_Date.split('-')
    end_split_date = end_Date.split('-')
    event_start_date = datetime(int(start_split_date[0]), int(start_split_date[1]), int(start_split_date[2]), 00, 00, 00, 0)
    event_start_date = pytz.UTC.localize(event_start_date).isoformat()

    event_end_date = datetime(int(end_split_date[0]), int(end_split_date[1]), int(end_split_date[2]), 23, 59, 59, 999999)
    event_end_date = pytz.UTC.localize(event_end_date).isoformat()

    events_result = api_service.events().list(calendarId='primary', timeMin=event_start_date,timeMax=event_end_date, timeZone="UTC").execute()
    return events_result.get('items', [])

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
        # token=""
        # with open('token.json', 'r') as token:
        #     token = token.read()
        # request_url="https://www.googleapis.com/oauth2/v3/userinfo?access_token={"+token+"}"
        # r=requests.get(request_url)
        # print(r.text)
        service = build('calendar', 'v3', credentials=creds)
        qurey=4
        event_dict_list=[]
        list_of_events=[]
        while (qurey!=0):
            print("0. Exit")
            print("1. Get all events")
            print("2. Get events by date")
            print("3. Get events by date range")
            qurey=int(input("Enter your choice: "))
            if qurey==1:
                events=get_events(service)
            elif qurey==2:
                start_Date=input("Enter start date YYYY-MM-DD: ")

                events=get_events_by_date(service,start_Date)
            elif qurey==3:
                start_Date=input("Enter start date YYYY-MM-DD: ")
                end_Date=input("Enter end date YYYY-MM-DD: ")
                events=get_events_by_date_range(service,start_Date,end_Date)
            elif qurey==0:
                break
            else:
                print("Invalid choice")
                continue
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
                        print(event_start_date,event_end_date,event_start_time,event_end_time)
                        title=event['summary']
                        creator=event['creator']['email']
                        attendees=[]
                        for attendee in event['attendees']:
                            attendees.append(attendee['email'])
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
                        print(event_list)
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
            print(df)

            df.to_csv("SavedCalendar.csv",index=False)
            if not events:
                print('No upcoming events found.')
                return
            qurey=0
        


    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()