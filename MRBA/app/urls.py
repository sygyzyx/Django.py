from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    path('EditRoom/<int:id>', views.editRoomView, name='editRoom'),
    path('DeleteRoom/<int:id>', views.deleteRoomBookingView, name='deleteRoom'),
    path('activate/<uidb64>/<token>', views.Activate, name='activate'),

    #######################################
    path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    path('password_change',auth_views.PasswordChangeView.as_view(),name="password_change"),
    path('password_change_done',auth_views.PasswordChangeDoneView.as_view(),name="password_change_done"),
    #########################################


    
]
