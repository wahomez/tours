from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.db.models.signals import post_save
from django.utils import timezone
import uuid

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=20)
    profile_pic = models.ImageField(blank=True, null=True)
    socials = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

#Create Profile when new User Signs Up
def createProfile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(createProfile, sender=User)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review")
    comment = models.TextField()
    uploaded_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Destination(models.Model):
    categories = [
        ('Excursions', 'Excursions'),
        ('Safari Tours', 'Safari Tours'),
        ('Farm Tours', 'Farm Tours'),
        ('Hiking and Adventures Tours', 'Hiking and Adventures Tours')
    ]
    category = models.CharField(max_length=50, choices=categories)
    description = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=250, null=True)
    duration = models.IntegerField(null=True)
    amount = models.IntegerField(null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, related_name="destination_review")
    about = models.TextField()
    notes = models.TextField()
    schedule = models.TextField()
    itinerary = models.TextField()
    poster = models.ImageField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="booking_user")
    tour = models.ForeignKey(Destination, on_delete=models.SET_NULL,null=True, related_name="booking_tour")
    slots = models.IntegerField()
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + str("-") + str(self.tour)
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, related_name="payment_booking")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.booking)
    
class Invoice(models.Model):
    invoice_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    tour = models.CharField(max_length=200)
    tour_date = models.CharField(max_length=200)
    price = models.IntegerField()
    slots = models.IntegerField()
    total = models.IntegerField()
    payment_date = models.DateTimeField()

    def __str__(self):
        return str(self.invoice_id)



