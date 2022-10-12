from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('Signup/', views.Signup, name='signup'),
    path('Dashboard', views.Dashboard, name='dashboard'),
    path('Login', views.LoginView, name='login'),
    path('Signout/', views.Signout, name='signout'),
    path('Status', views.Status, name='status'),
    path('Bookroom', views.BookRoom, name='book'),
    path('Room', views.roomView, name='room'),
    path('Account', views.accountView, name='account'),
    path('Grantmeet', views.grantMeetView, name='grantmeet'),
    path('CancelBooking/<int:id>', views.cancelBookingView, name='cancelbook'),
    path('EditRoom/<int:id>', views.editRoomView, name='editRoom')
]
