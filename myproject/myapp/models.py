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
    options=[('petrol','Petrol'),('diesel','Diesel'),('electric','Electric')]
    fuel=models.CharField(max_length=10,choices=options,null=True)
    description=models.TextField(null=True)  
    image=models.ImageField(upload_to='images/',blank=True,null=True)  
    status_options=[('available','Available'),('sold','Sold')]
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
    status_options=[('pending','Pending'),('confirmed','Confirmed'),('cancelled','Cancelled')]
    status=models.CharField(max_length=10,choices=status_options,null=True)

    def __str__(self):
        return self.vehicle.model

class Purchase(models.Model):
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE,null=True,related_name='purchases')
    customer=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='purchases')
    purchase_date=models.DateField(null=True)
    price=models.DecimalField(null=True,max_digits=10,decimal_places=2)   
    status_options=[('completed','Completed'),('cancelled','Cancelled')]
    status=models.CharField(max_length=10,choices=status_options,null=True)

    def __str__(self):
        return self.vehicle.model
    

class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.receiver =User.objects.filter(is_superuser=True).first()
        super(Chat, self).save(*args, **kwargs)


