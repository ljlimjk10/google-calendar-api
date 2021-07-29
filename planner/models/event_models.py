from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey
from . import User
from datetime import datetime


class GCalendar(models.Model):
    calendarTitle = CharField(max_length=300, unique=True ,null=True)
    calendarId = CharField(verbose_name='Calendar Id', max_length=300, unique=True, null=True)
    createdBy = ForeignKey(User, null=True, on_delete=models.CASCADE)

class GCalendarEvent(models.Model):
    gCalendar = ForeignKey(GCalendar, null=True, on_delete=models.CASCADE, related_name='gCalendarEvent')
    eventTitle = CharField(verbose_name='Event title', max_length=300, null=True)
    location = CharField(max_length=300, null=True)
    description = TextField(blank=True, null=True)
    startDateTime = DateTimeField(null=True)
    endDateTime = DateTimeField(null=True)
    createdBy = ForeignKey(User, null=True, verbose_name='Created by', on_delete=models.CASCADE, related_name='created_by')
    

    def __str__(self):
        return self.eventTitle
