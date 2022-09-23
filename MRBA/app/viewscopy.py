from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from app.models import Room, Room_Name 
from app.forms import RoomForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from datetime import datetime


def index(request):
    room = RoomForm()
    context = {'room': room}
    # import ipdb
    # ipdb.set_trace()
    return render(request, 'index.html', context)
    # if request.user == User.objects.get(username = request.user):
    #     return redirect('dashboard')

def dashboard(request):
    if request.user.is_authenticated:
        room = RoomForm()
        bookedrooms = Room.objects.all()
        context = {'room':room, 'booked':bookedrooms}
        if request.method == 'POST':
            print(list(request.POST.items()))
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in')
                if user.groups.filter(name='manager'):
                    #Displays Manager.html only to users assigned the GROUP as manager in admin site
                    return render(request, 'meetOnManager.html', context)
                    
                if user.groups.filter(name='user'):
                    return render(request, 'dashboard.html', context)
            else:
                messages.error(request, 'Please enter a valid Username and Password')
                return redirect('/')
    return render(request, 'dashboard.html', context)

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
            group = Group.objects.get(name='user') 
            group.user_set.add(user)
            user.save()
            messages.success(request, 'You can now a registered User !! Please continue to Login')
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
        #from the input field in index.html we only take HOUR and MINUTES so "%H:%M"yyyyyyy
        if Room.objects.filter(room_Name_id = room_id) & Room.objects.filter(room_book_date = date):    
            meetingTimeRange = Room.objects.values_list('meeting_start_time','meeting_end_time')
            for i in meetingTimeRange:
                start_time = int(i[0].strftime("%H%M"))
                end_time = int(i[1].strftime("%H%M"))
                if session_startStrf_time in range(start_time,end_time) or session_endStrf_time in range(start_time,end_time):
                    messages.error(request, 'Sorry This room is Booked')
                    return redirect('/')
                else:
                    availability = True
                    messages.success(request, 'Room available')
                    roomName = Room_Name.objects.get(id = room_id)
                    user = request.user
                    context = {'availability' : availability, 'roomName':roomName, 'Date': date, 'bookStartTime':session_start_time, 'bookEndTime': session_end_time,'User': user , 'room': room }
                    if request.user.is_anonymous:
                        return render(request,'index.html', context)
                    else:
                        return render(request,'dashboard.html', context)
            else:
                availability = True
                messages.success(request, 'Room available')
                roomName = Room_Name.objects.get(id = room_id)
                user = request.user
                context = {'availability' : availability, 'roomName':roomName, 'Date': date, 'bookStartTime':session_start_time, 'bookEndTime': session_end_time,'User': user , 'room': room }
                if request.user.is_anonymous:
                    return render(request,'index.html', context)
                else:
                    return render(request,'dashboard.html', context)

        else:
            availability = True
            messages.success(request, 'Room available')
            roomName = Room_Name.objects.get(id = room_id)
            user = request.user
            context = {'availability' : availability, 'roomName':roomName, 'Date': date, 'bookStartTime':session_start_time, 'bookEndTime': session_end_time,'User': user , 'room': room }
            if request.user.is_anonymous:
                return render(request,'index.html', context)
            else:
                return render(request,'dashboard.html', context)
    else:
        messages.error(request, 'Error')
        return redirect('/')    

def bookroom(request):
    if request.method == "POST":
        # import ipdb
        # ipdb.set_trace()
        name = request.POST.get('roomName')
        room_id = Room_Name.objects.filter(room_Name = name).values('id')
        date = request.POST.get('Date')
        room = RoomForm()
        
        #TIME_CONVERSION
        #START_TIME
        time_StartTime_inapt = request.POST.get('bookStartTime')
        time_StartTime_processed = time_StartTime_inapt.replace('.','').upper()
        time_StartTime_processed_2 = datetime.strptime(time_StartTime_processed, "%I:%M %p")
        result_StartTime_time = datetime.strftime(time_StartTime_processed_2, "%H:%M")

        #END_TIME
        time_EndTime_inapt = request.POST.get('bookEndTime')
        time_EndTime_processed = time_EndTime_inapt.replace('.','').upper()
        time_EndTime_processed_2 = datetime.strptime(time_EndTime_processed, "%I:%M %p")
        result_EndTime_time = datetime.strftime(time_EndTime_processed_2, "%H:%M")
        
        user = request.user
        bookRoom = Room.objects.create(room_Name_id = room_id,room_book_date = date, meeting_start_time = result_StartTime_time, meeting_end_time= result_EndTime_time, room_booked_by_user= user )
        bookRoom.save()
        context = {'room':room}
        messages.success(request, 'You Have Booked a room')
        return render(request, 'dashboard.html', context)

def signout(request):
    logout(request)
    messages.warning(request, 'You are logged out')
    return redirect('/')