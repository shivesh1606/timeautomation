
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