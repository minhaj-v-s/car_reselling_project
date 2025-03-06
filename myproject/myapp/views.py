from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import User
import re
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# Create your views here.

# def msg(request):
#     return HttpResponse("Hello World")

def home(request):
    return render(request, 'home.html')

def registration(request):
    return render(request,"registration.html")

def login(request):
    return render(request,"login.html")

def cars(request):
    return render(request,"cars.html")

def car_description(request):
    return render(request,"car_description.html")

def book_appointment(request):
    return render(request,"book_appointment.html")

def register(request):
    errors = {}

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        cpassword = request.POST.get("cpassword", "")
        password = request.POST.get("password", "")

        # Name validation (Only letters and spaces)
        if not re.match(r'^[A-Za-z\s]+$', name):
            errors["name"] = "Name should contain only letters and spaces."

        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            errors["email"] = "Invalid email format."

        # Phone number validation (Only 10 digits)
        if not re.match(r'^\d{10}$', phone):
            errors["phone"] = "Enter a valid 10-digit phone number."

        # Password validation (At least 8 chars, 1 uppercase, 1 number, 1 special character)
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', cpassword):
            errors["cpassword"] = "Password must be 8+ characters with 1 uppercase, 1 number, 1 special character."

        # Confirm password validation
        if cpassword != password:
            errors["password"] = "Passwords do not match."

        # If no errors, save user to DB
        if not errors:
            User.objects.create(
                name=name,
                email=email,
                phone=phone,
                password=password  
            )
            messages.success(request, "Registration successful! You can now log in.")  # ✅ Success message
            return redirect("register")  # Reload form with success message

    return render(request, "registration.html", {"errors": errors})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User  # Import your custom User model

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)  # Check if user exists
            if user.password == password:  # Validate password
                request.session['user_id'] = user.id  # Store user ID in session
                request.session['user_name'] = user.name  # Store user name in session
                messages.success(request, "Login successful!")
                return redirect('home')  # Redirect to home page
            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, 'login.html')



def logout_view(request):
    request.session.flush()  # Clear session
    return redirect("home")