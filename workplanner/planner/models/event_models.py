from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField
from django.db.models.fields.related import ForeignKey, OneToOneField
from . import User

class Event(models.Model):
    time_created = DateTimeField(auto_now_add=True)
    event_title = CharField(verbose_name='Event title', max_length=300, null=True)
    event_description = TextField(verbose_name='Event description', blank=True, null=True)
    created_by = ForeignKey(User, verbose_name='Created by', on_delete=models.PROTECT)

    class Meta:
        ordering = ['time_created', 'created_by']
        