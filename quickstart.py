from __future__ import print_function
import datetime
from os import path
import httplib2
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import googleapiclient.discovery
import os
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'serviceaccountcredentials.json'
SUBJECT_EMAIL = os.getenv("EMAIL")
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject=SUBJECT_EMAIL)
service = googleapiclient.discovery.build('calendar','v3',credentials=credentials)


class GoogleCalendar:
    
    
    def getCalendarList(self):
        calendar_list = service.calendarList().list().execute()
        for calendar_list_entry in calendar_list['items']:
            print(calendar_list_entry['summary'])
    
    
    def getCalendarId(self, title):
        '''Returns the calendars on the user's calendar list'''
        calendar_list = service.calendarList().list().execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == title:
                print(f"Calender:{title} found")
                self.calendar_id = calendar_list_entry['id']
                
    
    def createCalendar(self,title:str):
        '''Creates a secondary calendar'''
        calendar={
            'summary' : title,
            'timeZone' : 'Asia/Singapore'
        }
        created_calendar = service.calendars().insert(body=calendar).execute()
    
    def updateCalendar(self,title:str,updated_title:str):
        '''Updates metadata for a calendar'''
        self.getCalendarId(title)
        calendar_to_be_updated = service.calendars().get(calendarId=self.calendar_id).execute()
        calendar_to_be_updated['summary'] = updated_title
        updated_calendar = service.calendars().update(calendarId=self.calendar_id, body=calendar_to_be_updated).execute()
        

    def deleteCalendar(self, title:str):
        '''Deletes a secondary calendar'''
        self.getCalendarId(title)
        service.calendars().delete(calendarId=self.calendar_id).execute()



abc = GoogleCalendar()
# abc.createCalendar('Test Case')
# abc.updateCalendar('Test Case','Updated Test Case')
abc.getCalendarList()


