from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from app.models import Room as Rooms
from app.forms import RoomForm
from django.contrib.auth import authenticate, login, logout
from datetime import datetime


def index(request):
    room = RoomForm()
    context = {'room': room}
    # import ipdb
    # ipdb.set_trace()
    if request.user.is_anonymous:
        return render(request, 'index.html', context)
    if request.user == User.objects.get(username = request.user):
        return redirect('dashboard')

def dashboard(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in')
            return render(request, 'room.html')
        else:
            messages.error(request, 'Please enter a valid Username and Password')
            return redirect('/')
    return render(request, 'room.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if User.objects.filter(username = username).exists():
            messages.error(request, 'Username already Exists')
            return redirect('/')
        if pass1 != pass2:
            messages.error(request,'Please enter matching passwords')
            return redirect('/')
        else:
            user = User.objects.create_user(username = username, first_name = f_name, last_name = l_name, email = email, password = pass1)
            user.save()
            messages.success(request, 'SUCCESS')
            return redirect('/')    
    return redirect('/')

def signout(request):
    logout(request)
    messages.warning(request, 'You are logged out')
    return redirect('/')

def status(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_Name')
        date = request.POST.get('datePicker')
        start_time = datetime.strptime(request.POST.get('startTime'),"%H:%M")
        end_time = datetime.strptime(request.POST.get('endTime'), "%H:%M")
        #since from the input field in index.html we only take HOUR and MINUTES so "%H:%M"
        if Rooms.objects.filter(room_Name_id = room_id):
            if Rooms.objects.filter(room_book_date = date):
                if Rooms.objects.filter(meeting_start_time__range=(start_time, end_time)): #USE Q Method
                    if Rooms.objects.filter(meeting_end_time__range=(start_time,end_time)):
                        # if Rooms.objects.filter(start_time = range(meeting_start_time, meeting_end_time)):   (1-6)  2-3
                        messages.error(request, 'Room Booked')
                        return redirect('/')
                    else:
                        messages.success(request,'Not Booked')
                        print('Not Booked')
                        return redirect('/')
    else:
        messages.error('Error')
        return redirect('/')
    return redirect('/')

    