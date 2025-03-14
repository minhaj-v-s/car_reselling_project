from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=200,null=True)
    phone = models.CharField(max_length=15,null=True)
    password = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name
    
class Vehicle(models.Model):
    brand=models.CharField(max_length=200,null=True)
    model=models.CharField(max_length=200,null=True)
    year=models.IntegerField(null=True)
    price=models.DecimalField(null=True,max_digits=10,decimal_places=2)
    options=[('Petrol','Petrol'),('Diesel','Diesel'),('Electric','Electric')]
    kilometers = models.IntegerField(null=True)
    fuel=models.CharField(max_length=10,choices=options,null=True)
    transmission_options = [('Manual', 'Manual'), ('Automatic','Automatic'), ('Semi Automatic','Semi Automatic')]
    transmission = models.CharField(max_length=30, choices=transmission_options,null=True)
    description=models.TextField(null=True)  
    image=models.ImageField(upload_to='images/',blank=True,null=True)  
    status_options=[('Available','Available'),('Sold','Sold')]
    status=models.CharField(max_length=10,choices=status_options,null=True) 

    def __str__(self):
        return self.model

class VehicleImage(models.Model):
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE,null=True,related_name='images')
    image=models.ImageField(upload_to='images/',blank=True,null=True)

    def __str__(self):
        return self.vehicle.model

class Appointment(models.Model):
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE,null=True,related_name='appointments')
    customer=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='appointments')
    app_date=models.DateField(null=True)
    app_time=models.TimeField(null=True)
    status_options=[('Pending','Pending'),('Confirmed','Confirmed'),('Cancelled','Cancelled')]
    status=models.CharField(max_length=10,choices=status_options,null=True,default='Pending')

    def __str__(self):
        return f"{self.vehicle.model} - {self.status}" 

class Purchase(models.Model):
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE,null=True,related_name='purchases')
    customer=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='purchases')
    purchase_date=models.DateField(null=True)
    price=models.DecimalField(null=True,max_digits=10,decimal_places=2)   
    status_options=[('Completed','Completed'),('Cancelled','Cancelled')]
    status=models.CharField(max_length=10,choices=status_options,null=True)

    def __str__(self):
        return self.vehicle.model
    

from django.db import models
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True)
    message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Chat from {self.sender} to {self.receiver} at {self.timestamp}"

    def clean(self):
        if self.sender == self.receiver:
            raise ValidationError("Sender and receiver cannot be the same user.")

    def save(self, *args, **kwargs):
        super(Chat, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'


