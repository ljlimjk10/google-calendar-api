import os
import googleapiclient.discovery
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

class GoogleCalendar:
    
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        SERVICE_ACCOUNT_FILE = 'serviceaccountcredentials.json'
        SUBJECT_EMAIL = os.getenv("EMAIL")
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject=SUBJECT_EMAIL)
        self.service = googleapiclient.discovery.build('calendar','v3',credentials=credentials)

    def getCalendarList(self):
        '''Get title of all calendars in user'''
        calendar_list = self.service.calendarList().list().execute()
        for calendar_list_summary in calendar_list['items']:
           return calendar_list_summary['summary']
    
    
    def getCalendarId(self,calendar_title:str):
        '''Returns calendarId of specific calendar'''
        calendar_list = self.service.calendarList().list().execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == calendar_title:
                print(f"Calender:{calendar_title} found")
                self.calendar_id = calendar_list_entry['id']
                
    
    def createCalendar(self,calendar_title:str):
        '''Creates a secondary calendar'''
        calendar={
            'summary': calendar_title,
            'timeZone': 'Asia/Singapore'
        }
        created_calendar = self.service.calendars().insert(body=calendar).execute()
    
    def updateCalendar(self,calendar_title:str,updated_calendar_title:str):
        '''Updates metadata for a calendar'''
        self.getCalendarId(calendar_title)
        calendar_to_be_updated = self.service.calendars().get(calendarId=self.calendar_id).execute()
        calendar_to_be_updated['summary'] = updated_calendar_title
        updated_calendar = self.service.calendars().update(calendarId=self.calendar_id, body=calendar_to_be_updated).execute()
        

    def deleteCalendar(self,calendar_title:str):
        '''Deletes a secondary calendar'''
        self.getCalendarId(calendar_title)
        self.service.calendars().delete(calendarId=self.calendar_id).execute()


class GoogleCalendarEvent:

    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        SERVICE_ACCOUNT_FILE = 'serviceaccountcredentials.json'
        SUBJECT_EMAIL = os.getenv("EMAIL")
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject=SUBJECT_EMAIL)
        self.service = googleapiclient.discovery.build('calendar','v3',credentials=credentials)

    def getCalendarId(self,calendar_title:str):
        '''Returns calendarId of specific calendar'''
        calendar_list = self.service.calendarList().list().execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == calendar_title:
                print(f"Calender:{calendar_title} found")
                self.calendar_id = calendar_list_entry['id']

    def getCalendarEventId(self,calendar_title:str,event_title:str):
        self.getCalendarId(calendar_title)
        events = self.service.events().list(calendarId=self.calendar_id).execute()
        for event in events['items']:
            if event['summary'] == event_title:
                print(f"Event:{event_title} found")
                self.event_id = event['id']

    def getCalendarEventList(self,calendar_title:str):
        """Returns events on the specified calendar"""
        self.getCalendarId(calendar_title)
        events = self.service.events().list(calendarId=self.calendar_id).execute()
        for event in events['items']:
            print(event['summary'])

    def createCalendarEvent(self,calendar_title:str,event_title:str,location:str,description:str,start_date:str,start_time:str,end_date:str,end_time:str):
        """Creates an event"""
        self.getCalendarId(calendar_title)
        event = {
            'summary': event_title,
            'location': location,
            'description': description,
            'start':{
                'dateTime': start_date+'T'+start_time,
                'timeZone': 'Asia/Singapore'
            },
            'end':{
                'dateTime': end_date+'T'+end_time,
                'timeZone': 'Asia/Singapore'
            }
        }

        event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
        print("Event Created")

    def updateCalendarEvent(self,calendar_title=None,event_title=None,location=None,description=None,start_date=None,start_time=None,end_date=None,end_time=None):
        self.getCalendarEventId(calendar_title, event_title)
        event = self.service.events().get(calendarId=self.calendar_id, eventId=self.event_id).execute()
        if event_title:
            event['summary'] = event_title
        
        if location:
            event['location'] = location
        
        if description:
            event['description'] = description
        
        if start_date:
            if start_time:
                event['start']['dateTime'] = start_date+'T'+start_time
            else:
                print("Please provide start time")
                event['start']['dateTime'] = start_date+'T'+start_time
        
        if start_time:
            if start_date:
                 event['start']['dateTime'] = start_date+'T'+start_time
            else:
                print("Please provide start date")
                event['start']['dateTime'] = start_date+'T'+start_time

        if end_date:
            if end_time:
                event['end']['dateTime'] = end_date+'T'+end_time
            else:
                print("Please provde end time")
                event['end']['dateTime'] = end_date+'T'+end_time
        
        if end_time:
            if end_date:
                event['end']['dateTime'] = end_date+'T'+end_time
            else:
                print("Please provde end date")
                event['end']['dateTime'] = end_date+'T'+end_time

        updated_event = self.service.events().update(calendarId=self.calendar_id, eventId=self.event_id, body=event).execute()
        

        







