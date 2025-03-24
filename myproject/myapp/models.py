from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta
from django.core.exceptions import ValidationError
from datetime import datetime, time, timedelta
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=200,null=True)
    phone = models.CharField(max_length=15,null=True)
    password = models.CharField(max_length=200,null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.name
    
    def is_otp_valid(self):
        """"Check if OTP is still valid (within 15 minutes)"""
        if not self.otp or not self.otp_created_at:
            return False
        
        #OTP is valid for 15 minutes
        expiry_time = self.otp_created_at + timedelta(minutes=15)
        return timezone.now() <= expiry_time
    
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

# class Appointment(models.Model):
#     vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE,null=True,related_name='appointments')
#     customer=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='appointments')
#     app_date=models.DateField(null=True)
#     app_time=models.TimeField(null=True)
#     status_options=[('Pending','Pending'),('Confirmed','Confirmed'),('Cancelled','Cancelled')]
#     status=models.CharField(max_length=10,choices=status_options,null=True,default='Pending')


#     def __str__(self):
#         return f"{self.vehicle.model} - {self.status}" 
    
#     def save(self, *args, **kwargs):

#         # Check for overlapping appointments when creating or updating

#         if not self.pk or (self.pk and (self._state.adding or self.status != 'Cancelled')):

#             # Calculate a time window (1 hour before and after)

#             # time_obj = datetime.strptime(self.app_time, "%H:%M").time()
#             time_obj =self.app_time

#             hour_before = (datetime.combine(datetime.today(), time_obj) - timedelta(hours=1)).time()

#             hour_after = (datetime.combine(datetime.today(), time_obj) + timedelta(hours=1)).time()

            

#             # Find overlapping appointments

#             overlapping = Appointment.objects.filter(

#                 app_date=self.app_date,

#                 status__in=['Pending', 'Confirmed'],  # Only consider active appointments

#             ).exclude(pk=self.pk)  # Exclude self when updating

            

#             # Check if any appointment falls within the 1-hour window

#             for appt in overlapping:

#                 appt_time = appt.app_time

#                 if hour_before <= appt_time <= hour_after:

#                     # If this is a new appointment or an update that would create a conflict

#                     if self._state.adding:

#                         raise ValidationError("This time slot conflicts with an existing appointment within a 1-hour window.")

        

#         super(Appointment, self).save(*args, **kwargs)




class Appointment(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, related_name='appointments')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='appointments')
    app_date = models.DateField(null=True)
    app_time = models.TimeField(null=True)
    status_options = [('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')]
    status = models.CharField(max_length=10, choices=status_options, null=True, default='Pending')

    def __str__(self):
        return f"{self.vehicle.model} - {self.status}"

    def save(self, *args, **kwargs):
        if self.app_date and self.app_time:
            # Convert string time to time object if necessary
            if isinstance(self.app_time, str):
                try:
                    self.app_time = datetime.strptime(self.app_time, "%H:%M").time()  # 24-hour format
                except ValueError:
                    self.app_time = datetime.strptime(self.app_time, "%I:%M %p").time()  # 12-hour format

            if self._state.adding or self.status != 'Cancelled':
                time_obj = self.app_time  # Now it's guaranteed to be a time object

                # Calculate 1-hour before and after window
                hour_before = (datetime.combine(datetime.today(), time_obj) - timedelta(hours=1)).time()
                hour_after = (datetime.combine(datetime.today(), time_obj) + timedelta(hours=1)).time()

                # Find overlapping appointments
                overlapping = Appointment.objects.filter(
                    app_date=self.app_date,
                    status__in=['Pending', 'Confirmed']
                ).exclude(pk=self.pk)

                for appt in overlapping:
                    if hour_before <= appt.app_time <= hour_after:
                        raise ValidationError("This time slot conflicts with an existing appointment within a 1-hour window.")

        super(Appointment, self).save(*args, **kwargs)


class Purchase(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase')
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE,null=True,related_name='purchases')
    customer=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='purchases')
    purchase_date=models.DateField(null=True)
    price=models.DecimalField(null=True,max_digits=10,decimal_places=2)   
    status_options=[('Completed','Completed'),('Cancelled','Cancelled')]
    status=models.CharField(max_length=10,choices=status_options,null=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase')

    def __str__(self):
        return f"{self.vehicle.model} purchased by {self.customer.name}"

    
    def save(self, *args, **kwargs):

        # Mark vehicle as sold when a purchase is created

        if self.status == 'Completed' and self.vehicle.status != 'Sold':

            self.vehicle.status = 'Sold'

            self.vehicle.save()

            

        super(Purchase, self).save(*args, **kwargs)
    

class Feedback(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, related_name='feedback')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    rating_options = [(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')]
    rating = models.IntegerField(choices=rating_options)
    comment = models.TextField()
    image = models.ImageField(upload_to='feedback_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_testimonial = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback from {self.customer.name} - {self.rating} stars"



from django.db import models
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# class Chat(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True)
#     message = models.TextField(null=True, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Chat from {self.sender} to {self.receiver} at {self.timestamp}"

#     def clean(self):
#         if self.sender == self.receiver:
#             raise ValidationError("Sender and receiver cannot be the same user.")

#     def save(self, *args, **kwargs):
#         super(Chat, self).save(*args, **kwargs)

#     class Meta:
#         ordering = ['-timestamp']
#         verbose_name = 'Chat Message'
#         verbose_name_plural = 'Chat Messages'

class Cancellation(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='cancellation')
    reason = models.TextField()
    cancelled_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Cancellation for {self.appointment.vehicle.model} - {self.appointment.customer.name}"
