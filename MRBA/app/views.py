from errno import ETIME
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from app.models import Room, Room_Name 
from app.forms import RoomForm
from django.db.models import Q
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
            room = RoomForm()
            context = {'room':room}
            login(request, user)
            messages.success(request, 'You are logged in')
            return render(request, 'bookRoom.html', context)
        else:
            messages.error(request, 'Please enter a valid Username and Password')
            return redirect('/')
    return render(request, 'bookRoom.html')

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

def status(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_Name')
        date = request.POST.get('datePicker')
        room = RoomForm()
        session_start_time = datetime.strptime(request.POST.get('startTime'),"%H:%M").time()
        session_startStrf_time = int(session_start_time.strftime("%H%M"))
        #strptime returns a datetime oject but adding .time() returns only the time object.
        session_end_time = datetime.strptime(request.POST.get('endTime'), "%H:%M").time()
        session_endStrf_time = int(session_end_time.strftime("%H%M"))
        #from the input field in index.html we only take HOUR and MINUTES so "%H:%M"
        # import ipdb
        # ipdb.set_trace()
        if Room.objects.filter(room_Name_id = room_id):
            if Room.objects.filter(room_book_date = date):    
                meetingTimeRange = Room.objects.values_list('meeting_start_time','meeting_end_time')
                print('#################################')
                for i in meetingTimeRange:
                    start_time = int(i[0].strftime("%H%M"))
                    end_time = int(i[1].strftime("%H%M"))
                    if session_startStrf_time in range(start_time,end_time) or session_endStrf_time in range(start_time,end_time):
                        messages.error(request, 'Sorry This room is Booked')
                        return redirect('/')
                    else: 
                        availability = True
                        messages.success(request, 'Room available')
                        # room = RoomForm()
                        roomName = Room_Name.objects.get(id = room_id)
                        user = request.user
                        context = {'availability' : availability, 'roomName':roomName, 'Date': date, 'bookStartTime':session_start_time, 'bookEndTime': session_end_time,'User': user , 'room': room }
                        if request.user.is_anonymous:
                            return render(request,'index.html', context)
                        else:
                            return render(request,'bookRoom.html', context)
        else:
            messages.success(request,'This Room is Not Booked For This Date')
            return redirect('/')
    else:
        messages.error(request, 'Error')
        return redirect('/')
    return redirect('/')

def bookroom(request):
    if request.method == "POST":
        name = request.POST.get('roomName')
        room_id = Room_Name.objects.filter(room_Name = name).values('id')
        date = request.POST.get('Date')
        STime = datetime.strptime(request.POST.get('bookStartTime'),"%H:%M").time()
        ETime = datetime.strptime(request.POST.get('bookEndTime'),"%H:%M").time()
        user = request.user
        bookRoom = Room.objects.create(room_Name_id = room_id,room_book_date = date, meeting_start_time = STime,meeting_end_time= ETime, room_booked_by_user= user )
        bookRoom.save()
        # import ipdb
        # ipdb.set_trace()
        # room_id = request.POST.get('room_Name')
        # date = request.POST.get('datePicker')
        # session_start_time = datetime.strptime(request.POST.get('startTime'),"%H:%M").time()
        # session_end_time = datetime.strptime(request.POST.get('endTime'), "%H:%M").time()
        # user = request.user
        # bookRoom = Room.objects.create(room_Name_id = room_id,room_book_date = date, meeting_start_time = session_start_time,meeting_end_time= session_end_time, room_booked_by_user= user )
        # bookRoom.save()
        messages.success('You Have Booked a room')
        return redirect('/')

def signout(request):
    logout(request)
    messages.warning(request, 'You are logged out')
    return redirect('/')