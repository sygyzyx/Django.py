from dataclasses import fields
from django.forms import ModelForm
from .models import Room, Room_Name


class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ['user',]

class Room(ModelForm):
    class Meta:
        model = Room_Name
        fields = '__all__'