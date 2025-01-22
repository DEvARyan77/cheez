from django.urls import path, include
from  . import views
from django.contrib import admin

urlpatterns = [
    path('', include('myApp.urls')),
    path('api/login', views.logins, name='loginapi'),
    path('api/signup', views.signups, name='signupapi'),
    path('api/validate', views.validate, name='validateapi'),
    path('api/search', views.search, name='searchapi'),
    path('api/friend', views.friend, name='friendapi'),
    path('chat/', views.chat, name='chat'),
]
