from datetime import datetime
from decimal import MAX_EMAX
from pytz import timezone
from rest_framework import serializers
from planner.models import GCalendar, GCalendarEvent
from planner.models import User
from rest_framework.generics import get_object_or_404
from planner.utils.google_calendar_service import GoogleCalendar, GoogleCalendarEvent


class CalendarSerializer(serializers.ModelSerializer):

    gCalendarEvent = serializers.StringRelatedField(many=True)
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = GCalendar
        fields = ['calendarTitle','calendarId', 'gCalendarEvent', 'owner']
        #COMMENT OUT TO IGNORE GOOGLE CALENDAR API
        # extra_kwargs = {"calendarId":{"read_only":True}}
        
    
    def create(self,validated_data):
        if self.is_valid():
            calendarTitle = validated_data.get("calendarTitle")
            #COMMENT OUT calendarId when google api in use
            calendarId = validated_data.get("calendarId")
            owner = validated_data.get("owner")
            #COMMENTED OUT TO IGNORE GOOGLE CALENDAR API 
            #calendarId = GoogleCalendar.createCalendar(self,calendarTitle)
            gCalendar = GCalendar.objects.create(
                calendarTitle = calendarTitle,
                calendarId = calendarId,
                owner = owner
                )
        return gCalendar
    
    def update(self,instance,validated_data):
        instance.updatedCalendarTitle = validated_data.get("calendarTitle",instance.calendarTitle)
        #COMMENTED OUT TO IGNORE GOOGLE CALENDAR API
        # getCalendarId = GoogleCalendar.getCalendarId(self,instance.calendarTitle)
        # calendarId = GoogleCalendar.updateCalendar(self,instance.calendarTitle,instance.updatedCalendarTitle)
        instance.calendarTitle = instance.updatedCalendarTitle
        instance.save()
        return instance

class CalendarEventSerializer(serializers.ModelSerializer):

    calendarTitle = serializers.CharField(max_length=200, write_only=True)
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = GCalendarEvent
        fields = "__all__"
        extra_kwargs = {"gCalendar":{"read_only":True}, "eventId":{"read_only":True}}
        depth = 1
    
    def create(self,validated_data):
        if self.is_valid():
            calendarTitle = validated_data.get("calendarTitle")
            gCalendar = get_object_or_404(GCalendar, calendarTitle=calendarTitle)
            gCalendar = validated_data.pop("gCalendar")
            eventTitle = validated_data.get("eventTitle")
            location = validated_data.get("location")
            description = validated_data.get("description")
            startDateTime = validated_data.get("startDateTime")
            startDateTimeIso = startDateTime.isoformat()
            endDateTime = validated_data.get("endDateTime")
            endDateTimeIso = endDateTime.isoformat()
            owner = validated_data.get("owner")
            #COMMENTED OUT TO IGNORE GOOGLE CALENDAR API
            # getCalendarId = GoogleCalendarEvent.getCalendarId(self, calendarTitle)
            # eventId = GoogleCalendarEvent.createCalendarEvent(self,calendarTitle,eventTitle,location,description,startDateTime,endDateTime)
            gcalendarevent = GCalendarEvent.objects.create(gCalendar=gCalendar,eventTitle=eventTitle,location=location,description=description,startDateTime=startDateTimeIso,endDateTime=endDateTimeIso,owner=owner)
            #COMMENTED OUT TO IGNORE GOOGLE CALENDAR API
            #gcalendarevent = GCalendarEvent.objects.create(gCalendar=gCalendar,eventId=eventId,eventTitle=eventTitle,location=location,description=description,startDateTime=startDateTimeIso,endDateTime=endDateTimeIso,createdBy=createdBy)
        return gcalendarevent

class CalendarEventUpdateSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = GCalendarEvent
        fields = '__all__'
        extra_kwargs = {"gCalendar":{"read_only":True}, "eventId":{"read_only":True}}
        depth = 1

    def update(self,instance,validated_data):
        if self.is_valid():
            instance.eventTitle = validated_data.get("eventTitle", instance.eventTitle)
            instance.location = validated_data.get("location", instance.location)
            instance.description = validated_data.get("description", instance.description)
            instance.startDateTime = validated_data.get("startDateTime", instance.startDateTime)
            instance.endDateTime = validated_data.get("endDateTime", instance.endDateTime)
            instance.eventId = validated_data.get("eventId")
            #COMMENTED OUT TO IGNORE GOOGLE CALENDAR API
            # gcalendar = GCalendar.objects.first()
            # calendar_id_field_name = "calendarId"
            # calendarId = getattr(gcalendar,calendar_id_field_name)
            # eventId = GoogleCalendarEvent.updateCalendarEvent(self,calendarId,instance.eventId,instance.eventTitle,instance.location,instance.description,instance.startDateTime,instance.endDateTime)
            instance.save()
            return instance
