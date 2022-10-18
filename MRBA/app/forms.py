from django.forms import ModelForm
from .models import Room, Room_Name


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['room_Name','meeting_start_time','room_book_date','meeting_end_time']

class Room_NameForm(ModelForm):
    class Meta:
        model = Room_Name
        fields = '__all__'