from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def login(request):
    response = render(request, 'login.html')
    response['Cache-Control'] = 'public, max-age=300'
    return response
def signup(request):
    response = render(request,'signup.html')
    response['Cache-Control'] = 'public, max-age=300'
    return response
def home(request):
    return render(request,'home.html')