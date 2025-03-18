#views.py:

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import User,Appointment
import re
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Vehicle
from django.db.models import Q

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User 
from .models import Vehicle, Appointment, Cancellation
from django.shortcuts import get_object_or_404




# Create your views here.

# def msg(request):
#     return HttpResponse("Hello World")

def home(request):
    return render(request, 'home.html')

def registration(request):
    return render(request,"registration.html")

def login(request):
    return render(request,"login.html")

# def cars(request):
#     cars = Vehicle.objects.all()
#     return render(request,"cars.html",{'cars':cars})

def cars(request):
    cars = Vehicle.objects.all()

    search_query = request.GET.get('search', '')
    fuel_type = request.GET.get('fuel', '')
    brand = request.GET.get('brand', '')
    model = request.GET.get('model', '')
    transmission = request.GET.get('transmission', '')

    if search_query:
        cars = cars.filter(
            Q(brand__icontains=search_query) | 
            Q(model__icontains=search_query)
            
        )

    if fuel_type:
        cars = cars.filter(fuel=fuel_type)

    if brand:
        cars = cars.filter(brand__icontains=brand)

    if brand:
        cars = cars.filter(brand__icontains=brand)  

    if model:
        cars = cars.filter(model__icontains=model)  

    if transmission:
        cars = cars.filter(transmission__icontains=transmission)    


    return render(request, "cars.html", {'cars': cars})


# def car_description(request,pk):
#     car = Vehicle.objects.get(id=pk)
#     return render(request,"car_description.html",{'car':car})



def book_appointment(request,pk):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to book an appointment.")
        return redirect("login")
    thisCar = Vehicle.objects.get(id=pk)
    userName = request.session['user_name']
    userId = request.session['user_id']
    if request.method == "POST":
        vehicle = Vehicle.objects.get(id=pk)
        customer = User.objects.get(id=userId)
        app_date = request.POST.get("app_date")
        app_time = request.POST.get("app_time")

        existing_appointment = Appointment.objects.filter(app_date=app_date, app_time=app_time).exists()

        if existing_appointment:
            messages.error(request, "This time slot is already taken. Please choose another time.")
        else:
            Appointment.objects.create(vehicle=vehicle, customer=customer, app_date=app_date, app_time=app_time)
            messages.success(request, "Appointment booked successfully!")

    return render(request,"book_appointment.html",{'thisCar':thisCar,'user':userName})

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

 # Import your custom User model

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



def user_dashboard(request):
    return render(request,"user_dashboard.html")

def user_appointments(request):
    userId = request.session.get('user_id')
    user = User.objects.get(id=userId)
    appointments = Appointment.objects.filter(customer=user).order_by('-app_date','-app_time')
    print("Appointments found:", appointments)
    return render(request, "user_dashboard.html", {"appointments": appointments})
    
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "POST":
        reason = request.POST.get("reason")
        if reason:
            Cancellation.objects.create(appointment=appointment, reason=reason)
            appointment.status = "Cancelled"
            appointment.save()
            messages.success(request, "Appointment cancelled successfully.")
        else:
            messages.error(request, "Please provide a reason for cancellation.")

    return render(request,"user_dashboard.html")  # Change to your actual user dashboard URL name



def logout_view(request):
    request.session.flush()  # Clear session
    return redirect("home")

def car_description(request, pk):
    thisCar = get_object_or_404(Vehicle, id=pk)
    images = thisCar.images.all()  # Fetch all images related to the car

    # Process description into points
    description_text = thisCar.description or ""
    description_points = []
    
    # Split by periods and filter out empty strings
    raw_points = [p.strip() for p in description_text.split('.') if p.strip()]
    description_points = raw_points

    return render(request, "car_description.html", {
        'car': thisCar,
        'thisCar': thisCar,  # You use both variable names in your template
        'images': images,
        'description_points': description_points  # Match the variable name in your template
    })


def delete_appointment(request,pk):
    record_id = pk
    record = Appointment.objects.get(id=record_id)
    record.delete()

    return render(request,"user_dashboard.html")


# In your view function
def home_view(request):
    context = {
        'active_page': 'home',
        # other context data
    }
    return render(request, 'home.html', context)


def contactUs(request):
    return render(request, 'contactUs.html')