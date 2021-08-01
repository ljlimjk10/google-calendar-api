import os
import googleapiclient.discovery
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_OAUTH")
SUBJECT_EMAIL = os.getenv("EMAIL")
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject=SUBJECT_EMAIL)
service = googleapiclient.discovery.build('calendar','v3',credentials=credentials)


class GoogleCalendar:
    
    def getCalendarList(self):
        '''Get title of all calendars in user'''
        calendar_list = service.calendarList().list().execute()
        for calendar_list_entry in calendar_list['items']:
           return calendar_list_entry['summary']
    
    
    def getCalendarId(self,calendarTitle:str):
        '''Returns calendarId of specific calendar'''
        calendar_list = service.calendarList().list().execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == calendarTitle:
                print(f"Calender:{calendarTitle} found")
                self.calendar_id = calendar_list_entry['id']
        return self.calendar_id
                
    
    def createCalendar(self,calendarTitle:str):
        '''Creates a secondary calendar'''
        calendar_metadata={
            'summary': calendarTitle,
            'timeZone': 'Asia/Singapore'
        }
        calendar = service.calendars().insert(body=calendar_metadata, fields='id').execute()
        calendarId = calendar.get('id')
        return calendarId

    def updateCalendar(self,calendarTitle:str,updatedCalendarTitle:str):
        '''Updates metadata for a calendar'''
        self.getCalendarId(calendarTitle)
        calendar_to_be_updated = service.calendars().get(calendarId=self.calendar_id).execute()
        calendar_to_be_updated['summary'] = updatedCalendarTitle
        calendar_updated = service.calendars().update(calendarId=self.calendar_id, body=calendar_to_be_updated).execute()
        return self.calendar_id
        

    def deleteCalendar(self,calendarTitle:str):
        '''Deletes a secondary calendar'''
        self.getCalendarId(calendarTitle)
        service.calendars().delete(calendarId=self.calendar_id).execute()


class GoogleCalendarEvent:

    def getCalendarId(self,calendarTitle:str):
        '''Returns calendarId of specific calendar'''
        calendar_list = service.calendarList().list().execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == calendarTitle:
                print(f"Calender:{calendarTitle} found")
                self.calendar_id = calendar_list_entry['id']
        return self.calendar_id 

    def getCalendarEventId(self,calendarTitle:str,eventTitle:str):
        self.getCalendarId(calendarTitle)
        events = service.events().list(calendarId=self.calendar_id).execute()
        for event in events['items']:
            if event['summary'] == eventTitle:
                print(f"Event:{eventTitle} found")
                self.event_id = event['id']

    def getCalendarEventList(self,calendarTitle:str):
        """Returns events on the specified calendar"""
        self.getCalendarId(calendarTitle)
        events = service.events().list(calendarId=self.calendar_id).execute()
        for event in events['items']:
            print(event['summary'])

    def createCalendarEvent(self,calendarTitle:str,eventTitle:str,location:str,description:str,startDateTime,endDateTime):
        """Creates an event"""
        self.getCalendarId(calendarTitle)
        event_metadata = {
            'summary': eventTitle,
            'location': location,
            'description': description,
            'start':{
                'dateTime': startDateTime,
                'timeZone': 'Asia/Singapore'
            },
            'end':{
                'dateTime': endDateTime,
                'timeZone': 'Asia/Singapore'
            }
        }

        event = service.events().insert(calendarId=self.calendar_id, body=event_metadata, fields='id').execute()
        eventId = event.get('id')
        return eventId

    def updateCalendarEvent(self,calendarId,eventId,eventTitle=None,location=None,description=None,startDateTime=None,endDateTime=None):

        event = service.events().get(calendarId=calendarId, eventId=eventId).execute()
        if eventTitle: 
            event['summary'] = eventTitle
        
        if location:
            event['location'] = location
        
        if description:
            event['description'] = description
        
        if startDateTime:
            event['start']['dateTime'] = startDateTime
        
        if endDateTime:
           event['end']['dateTime'] = endDateTime

        updated_event = service.events().update(calendarId=calendarId, eventId=eventId, body=event).execute()
        return eventId
        







