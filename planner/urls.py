from django.urls import path
from django.urls.resolvers import URLPattern
from planner import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('user/', views.user_views.UserList.as_view(), name='user-view'),
    path('user/<str:username>', views.user_views.UserDetails.as_view(), name='user-view'),
    path('login', obtain_auth_token, name='api-token-auth'),
    path('event', views.event_views.CalendarEventList.as_view(), name='event-view'),
    path('event/<str:eventTitle>', views.event_views.CalendarEventDetails.as_view(), name='event-view'),
    path('calendar', views.event_views.CalendarList.as_view(), name='calendar-view'),
    path('calendar/<str:calendarTitle>', views.event_views.CalendarDetails.as_view(), name='calendar-view')
]