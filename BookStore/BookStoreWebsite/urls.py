from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('Books', views.book, name='book'),
    path('Author', views.author, name='author'),
    path('Delete/<int:id>/', views.delete, name='delete'),
    path('Detail/<int:id>/', views.details, name='detail'),
    path('Edit/<int:id>/', views.edit, name='edit'),
    path('SignUp', views.signup, name='signup'),
    path('SignIn', views.signin, name='signin'),
    path('Signout', views.signout, name='signout')
]
