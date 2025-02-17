from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.contrib.auth import get_user_model



class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_cashier = models.BooleanField(default=False)

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_color = models.CharField(max_length=100)
    comment = models.TextField(max_length=5000, blank=True)
    cost_per_day = models.IntegerField(null=True, blank=True)
    is_payed = models.BooleanField(default=False)
    price = models.TextField(max_length=5000, blank=True)
    device = models.TextField(max_length=5000, blank=True)
    days_spent = models.CharField(null=True, blank=True, max_length=1000)
    total_cost = models.IntegerField(null=True, blank=True)
    register_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=100)
    reg_date = models.DateTimeField(auto_now_add=True)
    exit_date = models.DateTimeField(null=True, blank=True)  
    name = models.CharField(max_length=255, default="*")
    email = models.EmailField(default="*")  
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    payment_date = models.DateTimeField(blank=True, null=True) 
    location =  models.CharField(default='',max_length=10)
    payment_method = models.CharField(max_length=100, blank=True, null=True)  

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Meta:
    ordering = ['id']


class Payment(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, null= True,blank= True,choices=[
        ('Mpesa', 'Mpesa'),
        ('Credit Card', 'Credit Card'),
        ('PayPal', 'PayPal')
    ])
    payment_date = models.DateTimeField(null=True, blank=True)
    id = models.AutoField(primary_key=True)

    def _str_(self):
        return f"Payment of {self.amount} by {self.customer}"

class ParkingLocation(models.Model):
    name = models.CharField(max_length=100)  # Name of the parking area/slot
    section = models.CharField(max_length=50, null=True, blank=True)  # Section/Zone, if applicable
    is_occupied = models.BooleanField(default=False)  # Occupied status

    def __str__(self):
        return f"{self.name} - {self.section if self.section else 'General'}"
class VehicleManager(models.Manager):
    def active(self):
        return self.filter(parked_at__isnull=False)
class Vehicle(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    parked_at = models.CharField(max_length=50, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    location =  models.CharField(default='',max_length=10)
    parked_time = models.DateTimeField(auto_now_add=True)
    vehicle_type = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    # Default manager (this is automatically added by Django if not overridden)
    objects = models.Manager()

    # Custom manager (for specific queries)
    vehicles = VehicleManager()

    def __str__(self):
        return f'{self.owner} ({self.license_plate})'


    
def get_default_user():
    # Return a default user, or you can use a specific user by ID
    User = get_user_model()
    return User.objects.get(id=1)

class ParkingSlot(models.Model):
    slot_number = models.CharField(max_length=10, unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Slot {self.slot_number} ({'Available' if self.is_available else 'Occupied'})"

class VehicleLocation(models.Model):
    license_plate = models.CharField(max_length=15, unique=True)
    parking_slot = models.OneToOneField(ParkingSlot, on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # This establishes a one-to-many relationship with the User model
    town = models.CharField(max_length=100)

    def __str__(self):
            return self.license_plate