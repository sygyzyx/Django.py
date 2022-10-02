from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('signup/', views.Signup, name='signup'),
    path('dashboard', views.Dashboard, name='dashboard'),
    path('login', views.LoginView, name='login'),
    path('signout/', views.Signout, name='signout'),
    path('status', views.Status, name='status'),
    path('bookroom', views.BookRoom, name='book')
]
