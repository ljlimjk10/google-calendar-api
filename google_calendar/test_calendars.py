import unittest
from unittest.mock import Mock, patch
import googleapiclient.discovery
from google_calendar_service import GoogleCalendar 


class GoogleCalendarTest(unittest.TestCase):
    
    @patch('google_calendar_service.googleapiclient.discovery')
    def test_get_calendar_list(self, mock_discovery):
        calendar_list = mock_discovery.build.return_value.calendarList.return_value.list.return_value.execute.return_value = {

            "kind": "calendar#calendarList",
            "etag": "\"p33ocftm2tbmf20g\"",
            "nextSyncToken": "CPDH9sLq7PECEhNsamxpbWprMTBAZ21haWwuY29t",
            "items": [
                {
                    "kind": "calendar#calendarListEntry",
                    "etag": "\"1624289280626000\"",
                    "id": "addressbook#contacts@group.v.calendar.google.com",
                    "summary": "Birthdays",
                    "description": "Displays birthdays, anniversaries, and other event dates of people in Google Contacts.",
                    "timeZone": "Asia/Singapore",
                    "colorId": "13",
                    "backgroundColor": "#92e1c0",
                    "foregroundColor": "#000000",
                    "selected": True,
                    "accessRole": "reader",
                    "defaultReminders": [],
                    "conferenceProperties": {
                        "allowedConferenceSolutionTypes": [
                        "hangoutsMeet"
                        ]
                    }
                }
            ]
        }
                
            
        

        for calendar_list_summary in calendar_list['items']:
            self.assertEqual(calendar_list_summary['summary'], 'Birthdays')        



if __name__ == '__main__':
    unittest.main()


