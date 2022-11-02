from django.contrib import messages
from django.db.models import Q
from django.forms import EmailField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from app.models import Room, Room_Name 
from app.forms import RoomForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from .tokens import *


def Index(request):
    room = RoomForm()
    today = datetime.today()
    tomorrow = datetime.today() + timedelta(days=1)
    bookedrooms = Room.objects.all().filter(room_book_date = today)
    bookedroomsTomorrow = Room.objects.all().filter(room_book_date = tomorrow)
    context = {'room':room, 'bookedrooms':bookedrooms,'bookedroomsTomorrow':bookedroomsTomorrow}
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
    admin = False
    room = RoomForm()
    today = datetime.today()
    tomorrow = datetime.today() + timedelta(days=1)
    bookedrooms = Room.objects.all().filter(room_book_date = today)
    bookedroomsTomorrow = Room.objects.all().filter(room_book_date = tomorrow)
    user = request.user
    if User.objects.filter(username=user) & User.objects.filter(is_staff=True):
        admin = True
        contex = {
        'admin':admin,
        'bookedroomsTomorrow':bookedroomsTomorrow,
        'room':room, 
        'bookedrooms':bookedrooms, 
        'user':user
                }
        return render(request, 'dashboard.html', contex)
    context = {'room':room, 'bookedrooms':bookedrooms, 'user':user,'bookedroomsTomorrow':bookedroomsTomorrow,'admin':admin}
    if request.user.is_anonymous:
        return redirect('index')
    return render(request, 'dashboard.html', context)


def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        # if User.objects.filter(email = email).exists():
        #     messages.error(request, 'Email already in use')
        #     return redirect('index')
        if User.objects.filter(username = username).exists():
            messages.error(request, 'Username already Exists')
            return redirect('index')
        if pass1 != pass2:
            messages.error(request,'Please enter matching passwords')
            return redirect('index')
        else:
            user = User.objects.create_user(username = username, first_name = f_name, last_name = l_name, email = email, password = pass1, is_active=False)
            #USER IS SAVED BUT CANNOT LOGIN SINCE IS_ACTIVE IS FALSE
            group = Group.objects.get(name='user') 
            group.user_set.add(user)
            user.save()
            subject = 'Ready To Book Your Meeting ?'
            message = render_to_string('template_activate_account.html', {
                                        'user': user.username,
                                        'domain': get_current_site(request).domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': account_activation_token.make_token(user),
                                        'protocol': 'https' if request.is_secure() else 'http'
                                    })
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]
            send_mail( subject, message, email_from, recipient_list )
            messages.success(request, 'Please Check Your Email For Verification')
            return redirect('index')
    return redirect('index')


def Activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email verification. Now you can login to your account.')
        return redirect('index')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('index')


def Status(request):
    # import ipdb
    # ipdb.set_trace()
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
    adminRoom = Room.objects.all().order_by('room_book_date')
    if User.objects.filter(username=user) & User.objects.filter(is_staff=True):
        admin = True
        contex = {
        'admin':admin,
        'adminRoom': adminRoom
    }
        return render(request, 'adminRoom.html', contex)
    else:
        admin = False
        context={
            'admin':admin,
            'userRoom': userRoom
        }
        return render(request, 'userRoom.html', context)


def accountView(request):
    user = request.user
    if not user.is_anonymous:
        return render(request, 'account.html')
    else:
        return redirect('/')


def editRoomView(request, id):
    room = get_object_or_404(Room, id = id)
    form = RoomForm(request.POST or None, instance=room)
    context = {
            'form':form,
            'room':room
        }
    if form.is_valid():
        # import ipdb
        # ipdb.set_trace()
        user = request.user
        room_id = request.POST.get('room_Name')
        date = request.POST.get('room_book_date')
        # id = request.POST.get('id')
        #####
        time_StartTime_inapt = request.POST.get('meeting_start_time')    
        time_StartTime_processed = time_StartTime_inapt.replace('.','').upper()
        time_StartTime_processed_2 = datetime.strptime(time_StartTime_processed, "%H:%M:%S")
        StartTime = int(datetime.strftime(time_StartTime_processed_2, "%H:%M").replace(":",""))
        #####
        time_EndTime_inapt = request.POST.get('meeting_end_time')
        time_EndTime_processed = time_EndTime_inapt.replace('.','').upper()
        time_EndTime_processed_2 = datetime.strptime(time_EndTime_processed, "%H:%M:%S")
        EndTime = int(datetime.strftime(time_EndTime_processed_2, "%H:%M").replace(":",""))
              
        #########
        #userId = Room.objects.filter(id=id).values('room_booked_by_user')
        # for k in userId:
        #             if (k['room_booked_by_user']) != request.user.id or StartTime in range(meeting_start_time,meeting_end_time) or EndTime in range(meeting_start_time,meeting_end_time) or meeting_start_time in range(StartTime,EndTime) or meeting_end_time in range(StartTime,EndTime): 
        #                 messages.error(request,'Time range Unavailable')
        #                 return redirect ('room')
        #########

        if Room.objects.filter(room_Name_id = room_id) & Room.objects.filter(room_book_date = date):  
            meetingTimeRange = (Room.objects.filter(room_Name_id=room_id) & Room.objects.filter(room_book_date = date)).values_list('meeting_start_time','meeting_end_time')
            for i in meetingTimeRange:
                meeting_start_time = int(i[0].strftime("%H%M"))
                meeting_end_time = int(i[1].strftime("%H%M"))
                if StartTime in range(meeting_start_time,meeting_end_time) or EndTime in range(meeting_start_time,meeting_end_time) or meeting_start_time in range(StartTime,EndTime) or meeting_end_time in range(StartTime,EndTime): 
                    messages.error(request,'Time range Unavailable')
                    return redirect ('room')
            else:
                form.save()
                messages.success(request,'Room Edited Successfully')
                return redirect('room')
        else:
            form.save()
            messages.success(request,'Room Edited Successfully')
            return redirect('room')
    return render(request, 'editRoom.html',context)

    # if request.method == 'POST':
    #     user = request.user
    #     room_id = request.POST.get('room_Name')
    #     date = request.POST.get('datePicker')
    #     StartTime = datetime.strptime(request.POST.get('startTime'),"%H:%M").time()
    #     StartTime = int(StartTime.strftime("%H%M"))
    #     EndTime = datetime.strptime(request.POST.get('endTime'),"%H:%M").time()
    #     editedEndTime = int(EndTime.strftime("%H%M"))
    #     # if User.objects.filter(username=user) & User.objects.filter(is_staff=True):
    #     if Room.objects.filter(room_Name_id = room_id) & Room.objects.filter(room_book_date = date):  
    #         meetingTimeRange = (Room.objects.filter(room_Name_id=room_id) & Room.objects.filter(room_book_date = date)).values_list('meeting_start_time','meeting_end_time')
    #         for i in meetingTimeRange:
    #             meeting_start_time = int(i[0].strftime("%H%M"))
    #             meeting_end_time = int(i[1].strftime("%H%M"))
    #             if editedStartTime in range(meeting_start_time,meeting_end_time) or editedEndTime in range(meeting_start_time,meeting_end_time) or meeting_start_time in range(editedStartTime,editedEndTime) or meeting_end_time in range(editedStartTime,editedEndTime):         
    #                 messages.error(request, 'Sorry This room is Booked')
    #                 return redirect('room')
    #             else:
    #                 messages.success(request, 'hello')
    #                 print(form.data)
    #                 if form.is_valid():
    #                     form.save()
    #                     messages.success('Saved')
    #                 return redirect('room')
   
    # else:
    #     form = RoomForm(instance=room)
    #     context = {
    #             'form':form,
    #             'room':room
    #         }
    #     return render(request, 'editRoom.html',context)


def grantMeetView(request):
    if request.method == 'POST':
        roomId = request.POST.get('value')
        meetStartTime = request.POST.get('meetStartTime')
        meetEndTime = request.POST.get('meetEndTime')
        room = Room.objects.get(id=roomId)
        room.grant_meeting = True
        room.save()
        messages.success(request, 'Room Granted')
        return redirect('room')


def deleteRoomBookingView(request, id):
    user = request.user
    if User.objects.filter(username=user):
        room = Room.objects.get(id=id)
        room.delete()
        return redirect('room')
    else:
        messages.error(request, 'ERROR')
        return redirect('/')


def cancelBookingView(request, id):
    user = request.user
    if User.objects.filter(username=user):
        room = Room.objects.get(id = id)
        room.grant_meeting = False
        room.save()
        messages.success(request, 'Room Booking Cancelled')
        return redirect('room')


def Signout(request):
    logout(request)
    messages.warning(request, 'You are logged out')
    return redirect('index')