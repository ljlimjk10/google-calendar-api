from rest_framework import serializers
from planner.models import Event

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"
