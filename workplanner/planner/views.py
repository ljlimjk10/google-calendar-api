from django.shortcuts import render
from django.http import HttpResponse
from planner.models import User
from planner.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import mixins,generics



# Create your views here.
def homepage(request):
    return HttpResponse("Welcome to homepage")

class UserList(generics.GenericAPIView,
               mixins.ListModelMixin,
               mixins.CreateModelMixin,
               ):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        print("hello")
        return self.create(request, *args, **kwargs)


class UserDetails(generics.GenericAPIView,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
