from django.db import models
from django.contrib.auth.models import User

class booking(models.Model):
    user= models.ForeignKey(User,on_delete=models.SET_NULL, null=True,blank=True)
    EVENT_TYPE_CHOICES = [
        ('wedding', 'Wedding'),
        ('party', 'Party'),
        ('birthday', 'Birthday Party'), 
        ('corporate', 'Corporate Event'),
        ('charity', 'Charity Function'),
    ]
    eventname=models.CharField(max_length=100)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    date = models.DateField()
    guest_count = models.PositiveIntegerField()
    description=models.TextField()
    venue = models.CharField(max_length=200)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    

class Donation(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Credit/Debit Card', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
        ('PayPal', 'PayPal'),
    ]

    UPI_APP_CHOICES = [
        ('GPay', 'GPay'),
        ('PhonePe', 'PhonePe'),
        ('Paytm', 'Paytm'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES)
    upi_app = models.CharField(max_length=20, choices=UPI_APP_CHOICES, null=True, blank=True)
    upi_id = models.CharField(max_length=100, null=True, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount} - {self.payment_method}"

# Create your models here.
