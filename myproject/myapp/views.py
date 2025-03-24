#views.py:

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import User,Appointment,Cancellation,Purchase,Vehicle,Feedback
import re
from django.contrib.auth import authenticate
from .models import Vehicle
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User 
from django.core.mail import send_mail
from utils.email_service import send_booking_email, send_cancellation_email,send_purchase_notification_email
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Create your views here.

# def msg(request):
#     return HttpResponse("Hello World")

def home(request):
    # Get testimonials (feedback marked as testimonial with rating 4 or 5)
    testimonials = Feedback.objects.filter(is_testimonial=True).order_by('-created_at')[:6]
    return render(request, 'home.html',{'testimonials':testimonials})

# def home(request):
#     # Get testimonials (feedback marked as testimonial with rating 4 or 5)
#     # testimonials = Feedback.objects.filter(is_testimonial=True).order_by('-created_at')[:6]
#     return render(request, 'home.html')

def registration(request):
    return render(request,"registration.html")

def login(request):
    return render(request,"login.html")

# def cars(request):
#     cars = Vehicle.objects.all()
#     return render(request,"cars.html",{'cars':cars})

def cars(request):
    all_cars = Vehicle.objects.all()
    available_cars = all_cars.filter(status='Available')
    search_query = request.GET.get('search', '')
    fuel_type = request.GET.get('fuel', '')
    brand = request.GET.get('brand', '')
    model = request.GET.get('model', '')
    transmission = request.GET.get('transmission', '')

    if search_query:
        available_cars = available_cars.filter(
            Q(brand__icontains=search_query) | 
            Q(model__icontains=search_query)
            
        )

    if fuel_type:
        available_cars = available_cars.filter(fuel=fuel_type)

    if brand:
        available_cars = available_cars.filter(brand__icontains=brand)

    if brand:
        available_cars = available_cars.filter(brand__icontains=brand)  

    if model:
        available_cars = available_cars.filter(model__icontains=model)  

    if transmission:
        available_cars = available_cars.filter(transmission__icontains=transmission)   

      # Get sold cars
    sold_cars = all_cars.filter(status='Sold')

    # If filters are applied, also filter the sold cars to maintain consistency
    if search_query:
        sold_cars = sold_cars.filter(
            Q(brand__icontains=search_query) | 
            Q(model__icontains=search_query)
        )
    
    if fuel_type:
        sold_cars = sold_cars.filter(fuel=fuel_type)
       
    if brand:
        sold_cars = sold_cars.filter(brand__icontains=brand)
       
    if model:
        sold_cars = sold_cars.filter(model__icontains=model)

    if transmission:
        sold_cars = sold_cars.filter(transmission__icontains=transmission)

    return render(request, "cars.html", {
        'cars': available_cars,
        'sold_cars': sold_cars
    })


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

        # Calculate a time window (1 hour before and after)
        time_obj = timezone.datetime.strptime(app_time, "%H:%M").time()
        hour_before = (timezone.datetime.combine(timezone.datetime.today(), time_obj) - timedelta(hours=1)).time()
        hour_after = (timezone.datetime.combine(timezone.datetime.today(), time_obj) + timedelta(hours=1)).time()
        # Find overlapping appointments
        overlapping = Appointment.objects.filter(
            app_date=app_date,
            status__in=['Pending', 'Confirmed']  # Only consider active appointments
        )
        # Check if any appointment falls within the 1-hour window
        conflict = False
        for appt in overlapping:
            appt_time = appt.app_time
            if hour_before <= appt_time <= hour_after:
                conflict = True
                break
        if conflict:
            messages.error(request, "This time slot conflicts with an existing appointment. Please choose a time at least 1 hour apart from other appointments.")
        else:
            appointment = Appointment.objects.create(
                vehicle=vehicle, 
                customer=customer, 
                app_date=app_date, 
                app_time=app_time
            )
            messages.success(request, "Appointment booked successfully!")
            send_booking_email(appointment)

            # Store message in session to display once when redirected

            request.session['message_displayed'] = True

            return redirect('user_appointments')
        
    return render(request, "book_appointment.html", {'thisCar': thisCar, 'user': userName})

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
            # User(name = name, email = email, phone = phone, password = password ).save()
            messages.success(request, "Registration successful! You can now log in.")  # ✅ Success message
            return redirect("register")  # Reload form with success message

    return render(request, "registration.html", {"errors": errors})




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
    # Get a list of vehicles purchased by this user
    purchased_vehicles = Purchase.objects.filter(customer=user).values_list('vehicle_id', flat=True)
    return render(request, "user_dashboard.html", {
        "appointments": appointments,
        "purchased_vehicles": purchased_vehicles
    })
    
# def cancel_appointment(request, appointment_id):
#     appointment = get_object_or_404(Appointment, id=appointment_id)

#     if request.method == "POST":
#         reason = request.POST.get("reason")
#         if reason:
#             Cancellation.objects.create(appointment=appointment, reason=reason)
#             appointment.status = "Cancelled"
#             appointment.save()
#             messages.success(request, "Appointment cancelled successfully.")

#         else:
#             messages.error(request, "Please provide a reason for cancellation.")

#     return render(request,"user_dashboard.html")  # Change to your actual user dashboard URL name



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


def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "POST":
        reason = request.POST.get("reason")
        if reason:
            cancellation_time = timezone.now()
            Cancellation.objects.create(appointment=appointment, reason=reason)
            appointment.status = "Cancelled"
            appointment.save()
            messages.success(request, "Appointment cancelled successfully.")

            send_cancellation_email(appointment, reason, cancellation_time)
            # send_mail(
            #     "Booking Cancelled",
            #     f"The following  test drive details has been cancelled by the customer \n Appointment date: {appointment.app_date} \n Appointment time: {appointment.app_time}\n Vehicle: {appointment.vehicle.brand} {appointment.vehicle.model}. Customer Name: {appointment.customer.name}\n Reason: {reason}",
            #     "mtem7118@gmail.com",
            #     ["minhajshams3@gmail.com"],
            #     fail_silently=False,
            # )
        else:
            messages.error(request, "Please provide a reason for cancellation.")

        # Get updated appointments list
    user_id = request.session.get('user_id')
    if user_id:
        # Order appointments by date and time, newest first
        appointments = Appointment.objects.filter(customer_id=user_id).order_by('-app_date', '-app_time')
        context = {'appointments': appointments}
        return render(request, "user_dashboard.html", context)
    else:
        return redirect('login')
    

# In your view function
def home_view(request):
    context = {
        'active_page': 'home',
        # other context data
    }
    return render(request, 'home.html', context)



def mark_as_purchased(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == "POST":
        # Update appointment status
        appointment.status = "Completed"
        appointment.save()
        # Create purchase record
        purchase = Purchase.objects.create(
            vehicle=appointment.vehicle,
            customer=appointment.customer,
            price=appointment.vehicle.price,
            appointment=appointment
        )

        # Update vehicle status to Sold
        vehicle = appointment.vehicle
        vehicle.status = 'Sold'
        vehicle.save()

        # Collect feedback
        return redirect('submit_feedback', purchase_id=purchase.id)
    
    return redirect('user_appointments')


def submit_feedback(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    
    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Check if high rating (4 or 5) to mark as potential testimonial
        is_testimonial = int(rating) >= 4
        
        # Create feedback
        feedback = Feedback.objects.create(
            purchase=purchase,
            customer=purchase.customer,
            rating=int(rating),
            comment=comment,
            is_testimonial=is_testimonial  # Auto-mark high ratings as testimonials
        )

     # Send notification email to admin
        send_purchase_notification_email(purchase, feedback)
        messages.success(request, "Thank you for your feedback! Your purchase has been recorded.")
        # Set a flag to display the message only once

        request.session['message_displayed'] = True
        return redirect('user_appointments')
    
    return render(request, "submit_feedback.html", {'purchase': purchase})



@require_POST
@csrf_exempt
def clear_messages(request):
    """Clear all messages from the session"""
    storage = messages.get_messages(request)
    for _ in storage:
        # Iterating through the messages marks them as read
        pass
     # This ensures the storage is cleared
    storage.used = True

    return JsonResponse({'status': 'success'})


def contactUs(request):
    return render(request, 'contactUs.html')

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404, context={'exception': exception})
