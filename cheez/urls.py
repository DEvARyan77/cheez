# myproject/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('myApp.urls')),  # Includes your app's URLs
]
