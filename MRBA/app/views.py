from tokenize import group
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from app.models import Room, Room_Name 
from app.forms import RoomForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from datetime import datetime


def Index(request):
    room = RoomForm()
    today = datetime.today()
    bookedrooms = Room.objects.all().filter(room_book_date = today)
    context = {'room':room, 'bookedrooms':bookedrooms}

    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'index.html', context)


def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please enter a valid Username and Password')
            return redirect('/')
    

def Dashboard(request):
    room = RoomForm()
    today = datetime.today()
    bookedrooms = Room.objects.all().filter(room_book_date = today)
    user = request.user
    context = {'room':room, 'bookedrooms':bookedrooms, 'user':user}
    if request.user.is_anonymous:
        return redirect('index')
    return render(request, 'dashboard.html',context)


def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if User.objects.filter(username = username).exists():
            messages.error(request, 'Username already Exists')
            return redirect('index')
        if pass1 != pass2:
            messages.error(request,'Please enter matching passwords')
            return redirect('index')
        else:
            user = User.objects.create_user(username = username, first_name = f_name, last_name = l_name, email = email, password = pass1)
            group = Group.objects.get(name='user') 
            group.user_set.add(user)
            user.save()
            messages.success(request, 'You are now a registered User !! Please continue to Login')
            return redirect('index')    
    return redirect('index')


def Status(request):
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
            meetingTimeRange = (Room.objects.filter(room_Name_id=room_id) & Room.objects.filter(room_book_date = date)).values_list('meeting_start_time','meeting_end_time')
            for i in meetingTimeRange:
                meeting_start_time = int(i[0].strftime("%H%M"))
                meeting_end_time = int(i[1].strftime("%H%M"))
                if session_startStrf_time in range(meeting_start_time,meeting_end_time) or session_endStrf_time in range(meeting_start_time,meeting_end_time) or meeting_start_time in range(session_startStrf_time,session_endStrf_time) or meeting_end_time in range(session_startStrf_time,session_endStrf_time):         
                    #or condition for 'meeting_end_time' not so necessary
                    messages.error(request, 'Sorry This room is Booked')
                    return redirect('dashboard')
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
        return redirect('dashboard')    


def BookRoom(request):
    if request.method == "POST":
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
        messages.success(request, 'You Have Booked a room')
        return redirect('dashboard')


def roomView(request):
    user = request.user
    userRoom = Room.objects.filter(room_booked_by_user = user)
    adminRoom = Room.objects.all()
    if User.objects.filter(username=user) & User.objects.filter(is_staff=True):
        contex = {
        'adminRoom': adminRoom
    }
        return render(request, 'adminRoom.html', contex)
    else:
        context={
            'userRoom': userRoom
        }
        return render(request, 'rooms.html', context)


def accountView(request):
    return render(request, 'account.html')


def editRoomView(request, id):
    room = Room.objects.get(id = id)
    print(room)
    form = RoomForm(request.POST or None, instance=room)
    context = {
        'room':room,
        'form':form
    }
    return render(request, 'editroom.html', context)


def grantMeetView(request):
    if request.method == 'POST':
        roomId = request.POST.get('value')
        room = Room.objects.get(id=roomId)
        room.grant_meeting = True
        room.save()
        messages.success(request, 'Room Granted')
        return redirect('room')


def cancelBookingView(request, id):
    if request.method == 'POST':
        room = Room.objects.get(id = id)
        room.grant_meeting = False
        room.save()
        messages.success(request, 'Room Unbooked')
        return redirect('room')



def Signout(request):
    logout(request)
    messages.warning(request, 'You are logged out')
    return redirect('index')