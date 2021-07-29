from datetime import datetime
from decimal import MAX_EMAX
from pytz import timezone
from rest_framework import serializers
from planner.models import GCalendar, GCalendarEvent
from planner.models import User
from rest_framework.generics import get_object_or_404
from planner.utils.google_calendar_service import GoogleCalendar


class CalendarSerializer(serializers.ModelSerializer):

    gCalendarEvent = serializers.StringRelatedField(many=True)
    email = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = GCalendar
        fields = ['calendarTitle','calendarId', 'gCalendarEvent', 'email']
        #COMMENT OUT TO IGNORE GOOGLE CALENDAR API
        # extra_kwargs = {"calendarId":{"read_only":True}}
        extra_kwargs = {"createdBy":{"read_only":True}}
    
    def create(self,validated_data):
        if self.is_valid():
            calendarTitle = validated_data.get("calendarTitle")
            calendarId = validated_data.get("calendarId")
            #COMMENTED OUT TO IGNORE GOOGLE CALENDAR API 
            # calendarId = GoogleCalendar.createCalendar(self,calendarTitle)
            email = validated_data.get("email")
            createdBy = get_object_or_404(User, email=email)
            gCalendar = GCalendar.objects.create(
                calendarTitle = calendarTitle,
                calendarId = calendarId,
                createdBy = createdBy
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
    email = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = GCalendarEvent
        fields = "__all__"
        extra_kwargs = {"createdBy":{"read_only":True}, "gCalendar":{"read_only":True}}
    
    def create(self,validated_data):
        if self.is_valid():
            calendarTitle = validated_data.get("calendarTitle")
            gCalendar = get_object_or_404(GCalendar, calendarTitle=calendarTitle)
            eventTitle = validated_data.get("eventTitle")
            location = validated_data.get("location")
            description = validated_data.get("description")
            startDateTime = validated_data.get("startDateTime")
            startDateTimeIso = startDateTime.isoformat()
            endDateTime = validated_data.get("endDateTime")
            endDateTimeIso = endDateTime.isoformat()
            email = validated_data.get("email")
            createdBy = get_object_or_404(User, email=email)
            gcalendarevent = GCalendarEvent.objects.create(gCalendar=gCalendar,eventTitle=eventTitle,location=location,description=description,startDateTime=startDateTimeIso,endDateTime=endDateTimeIso,createdBy=createdBy)
        return gcalendarevent

