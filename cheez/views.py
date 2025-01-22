from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models.connection import collection
import json
import bcrypt
import re
import jwt
import datetime
from dotenv import load_dotenv
import os
from django.shortcuts import render

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
print(f"Loaded SECRET_KEY: {SECRET_KEY}")  # Debug print

@csrf_exempt
def chat(request):
    return render(request, 'chat.html')

@csrf_exempt
def logins(request):
    print("login")
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # Check if username and password are provided
        if not username or not password:
            return HttpResponse("Username and password are required", status=400)

        # Find the user in the database
        user = collection.find_one({"username": username})
        if not user:
            return HttpResponse("Invalid username", status=400)

        # Check if the password is correct
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return HttpResponse("Invalid password", status=400)

        # Generate JWT token
        payload = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return JsonResponse({'token': token})
    except Exception as e:
        print(f"Error during login: {e}")
        return HttpResponse("error", status=500)

@csrf_exempt
def signups(request):
    print("Signup")
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        friends = data.get('friends', [])
        # Check if username, password, or email is empty
        if not username or not password or not email:
            return HttpResponse("Username, password, and email are required", status=400)

        # Check if the username already exists
        if collection.find_one({"username": username}):
            return HttpResponse("Username already exists", status=400)

        # Validate email format
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return HttpResponse("Invalid email format", status=400)

        # Ensure the password meets the required length
        if len(password) < 8:
            return HttpResponse("Password must be at least 8 characters long", status=400)

        # Encrypt the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_data = {
            "username": username,
            "password": hashed_password.decode('utf-8'),
            "email": email,
            "friends": friends
        }

        collection.insert_one(user_data)
        print(f"User {username} signed up successfully")
        return HttpResponse("done")
    except Exception as e:
        print(f"Error during signup: {e}")
        return HttpResponse("error", status=500)

@csrf_exempt
def validate(request):
    try:
        data = json.loads(request.body)
        token = data.get('token')
        if not token:
            return HttpResponse("Token is required", status=400)
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return JsonResponse(payload)
    except Exception as e:
        print(f"Error during validation: {e}")
        return HttpResponse("Unauthorized", status=401)

@csrf_exempt
def search(request):
    try:
        data = json.loads(request.body)
        token = data
        if not token:
            return HttpResponse("Token is required", status=400)
        
        username = data.get('query')
        print(username)
        if not username:
            return HttpResponse("Username is required", status=400)
        
        # Use regex to search for usernames containing the search term
        users = collection.find({"username": {"$regex": username, "$options": "i"}}, {"username": 1, "_id": 0})
        users_list = [user['username'] for user in users]
        
        
        return JsonResponse(users_list, safe=False)
    except Exception as e:
        print(f"Error during search: {e}")
        return HttpResponse("error", status=500)

@csrf_exempt
def friend(request):
    try:
        data = json.loads(request.body)
        token = data.get('token')
        if not token:
            return HttpResponse("Token is required", status=400)
        
        # Validate the token
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return HttpResponse("Token has expired", status=401)
        except jwt.InvalidTokenError:
            return HttpResponse("Invalid token", status=401)
        
        username = payload['username']
        friend = data.get('friend')
        if not friend:
            return HttpResponse("Friend is required", status=400)
        
        # Split the friend string by commas
        friends_list = [f.strip() for f in friend.split(',')]
        
        # Fetch the current friends list
        user = collection.find_one({"username": username})
        if not user:
            return HttpResponse("User not found", status=404)
        
        current_friends = user.get('friends', [])
        
        # Filter out friends that are already in the current friends list
        new_friends = [f for f in friends_list if f not in current_friends]
        
        if not new_friends:
            return HttpResponse("No new friends to add", status=400)
        
        # Update the user's friends list in the database
        collection.update_one(
            {"username": username},
            {"$addToSet": {"friends": {"$each": new_friends}}}
        )
        
        return HttpResponse("Friends added successfully")
    except Exception as e:
        print(f"Error during adding friends: {e}")
        return HttpResponse("error", status=500)