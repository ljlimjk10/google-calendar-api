from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('user', views.UserList.as_view(), name='user-view'),
    path('user/<str:username>', views.UserDetails.as_view(), name='user-view'),
    path('login', obtain_auth_token, name='api-token-auth'),
    path('event', views.EventList.as_view(), name='event-view'),
    path('event/<str:event_title>', views.EventDetails.as_view(), name='event-view'),

]