from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.userLogin, name='dashboard'),
    path('signout', views.signout, name='signout'),
    path('status', views.status, name='status'),
    path('bookroom', views.bookroom, name='book')
]
