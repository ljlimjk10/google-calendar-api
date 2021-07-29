from planner import serializers
from planner.models import GCalendar, GCalendarEvent
from planner.serializers import CalendarEventSerializer, CalendarSerializer
from rest_framework.views import APIView
from rest_framework import mixins,generics,status
from rest_framework.response import Response
from planner.utils.google_calendar_service import GoogleCalendar


class CalendarList(generics.GenericAPIView,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    
    queryset = GCalendar.objects.all()
    serializer_class = CalendarSerializer
    lookup_field = "calendarTitle"

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CalendarDetails(generics.GenericAPIView,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    
    queryset = GCalendar.objects.all()
    serializer_class = CalendarSerializer
    lookup_field = "calendarTitle"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        GoogleCalendar.deleteCalendar(self, self.kwargs.get('calendarTitle'))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CalendarEventList(generics.GenericAPIView,
                mixins.ListModelMixin,
                mixins.CreateModelMixin):
    
    queryset = GCalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    lookup_field = "eventTitle"

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CalendarEventDetails(generics.GenericAPIView,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):

    queryset = GCalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    lookup_field = "eventTitle"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
