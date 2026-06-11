from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import viewsets

from quickstart.serializers import GroupSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
