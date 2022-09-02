from django.contrib import admin
from .models import Room, Room_Name

# Register your models here.
admin.site.register(Room),
admin.site.register(Room_Name)