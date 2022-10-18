
from django.db import models
from django.contrib.auth.models import User

class Password_Reset_Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password_reset_token = models.CharField(max_length=100)
    def __str__(self):
        return self.user.email

class Room_Name(models.Model):
    room_Name = models.CharField(max_length=122)
    def __str__(self):
        return self.room_Name

class Room(models.Model):
    room_Name = models.ForeignKey(Room_Name, on_delete=models.CASCADE)
    room_book_date = models.DateField()
    meeting_start_time = models.TimeField()
    meeting_end_time = models.TimeField()
    room_booked_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    grant_meeting = models.BooleanField(default = False)
    def __str__(self):
        return self.room_Name.room_Name
    


