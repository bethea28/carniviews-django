from django.shortcuts import render

# Create your views here.
# Import necessary modules and models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from google.oauth2 import id_token
from google.auth.transport import requests

# Replace with your Web Client ID
CLIENT_ID ="389796448834-lokv2d5vt75qbshil74f1t6c8hrajm48.apps.googleusercontent.com",

def verify_google_token(token):
    """Verifies the Google ID token."""
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        user_id = idinfo['sub']
        email = idinfo.get('email')
        name = idinfo.get('name')

        return {'user_id': user_id, 'email': email, 'name': name}

    except ValueError as e:
        print(f"Error verifying Google token: {e}")
        return None

@csrf_exempt
def googleAuth(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse the JSON data
            user_data = data.get('userData', {})  # Get the userData object
            id_token_value = user_data.get('data', {}).get('idToken') # Corrected path

            if not id_token_value:
                return JsonResponse({'message': 'idToken missing'}, status=400)

            google_user_info = verify_google_token(id_token_value)

            if google_user_info:
                # Find or create user in your Django database
                # Create a session or JWT
                return JsonResponse({'message': 'Google sign-in successful', 'user': google_user_info}, status=200)

            else:
                return JsonResponse({'message': 'Google sign-in failed'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)



# Define a view function for the login page
def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/')
        
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            user_data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            
            # Render the home page template with user data
            return render(request, 'login.html', {'user_data': user_data})
            # return redirect('/home/')
    
    # Render the login page template (GET request)
    return render(request, 'login.html')

# Define a view function for the registration page
def register_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
        
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/register/')
    
    # Render the registration page template (GET request)
    return render(request, 'register.html')


# Define a view function for the home page
def home(request):
    return render(request, 'home.html')