from django.shortcuts import render
from django.http import HttpResponse
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
