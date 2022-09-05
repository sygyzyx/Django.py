from django.forms import ModelForm
from .models import Room, Room_Name


class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ['user',]

class Room_NameForm(ModelForm):
    class Meta:
        model = Room_Name
        fields = '__all__'