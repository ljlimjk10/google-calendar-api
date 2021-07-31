from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey
from . import User
from datetime import datetime


class GCalendar(models.Model):
    calendarTitle = CharField(max_length=300, unique=True ,null=True)
    calendarId = TextField(verbose_name='Calendar Id', unique=True, null=True)
    owner = ForeignKey(User, null=True, on_delete=models.CASCADE)

class GCalendarEvent(models.Model):
    gCalendar = ForeignKey(GCalendar, related_name="gCalendarEvent", null=True, on_delete=models.CASCADE)
    eventTitle = CharField(verbose_name='Event title', max_length=300, null=True)
    eventId = TextField(verbose_name='Event Id', unique=True, null=True)
    location = CharField(max_length=300, null=True)
    description = TextField(blank=True, null=True)
    startDateTime = DateTimeField(null=True)
    endDateTime = DateTimeField(null=True)
    owner = ForeignKey(User, null=True, on_delete=models.CASCADE)

    #Change self.description to eventId when api is available
    def __str__(self):
        return '%s:%s'%(self.description,self.eventTitle)

#link GCalendar and GCalendarEvent