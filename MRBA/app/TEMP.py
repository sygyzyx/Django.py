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
                        return render(request,'dashboard.html', context)
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
                    return render(request,'dashboard.html', context)
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
                return render(request,'dashboard.html', context)
    else:
        messages.error(request, 'Error')
        return redirect('/')
