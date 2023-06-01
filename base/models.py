from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.db.models.signals import post_save
from datetime import datetime
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

# #Create Profile when new User Signs Up
# def createProfile(sender, instance, created, **kwargs):
#     if created:
#         user_profile = Profile(user=instance)
#         user_profile.save()

# post_save.connect(createProfile, sender=User)

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
    discount = models.IntegerField(blank=True, null=True)
    # review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, related_name="destination_review")
    about = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    schedule = models.TextField(null=True, blank=True)
    itinerary = models.TextField(null=True, blank=True)
    discounted_total = models.IntegerField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="tour_like", blank="true")
    poster = models.ImageField()

    #keep track of like count
    def number_of_likes(self):
        return self.likes.count()

    #calculate the amount after discount
    def save(self, *args, **kwargs):
        self.discounted_total = self.amount - self.discount

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review")
    tour = models.ForeignKey(Destination, null=True, on_delete=models.SET_NULL, related_name="tour_review")
    comment = models.TextField()
    uploaded_date = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.user.username

class Booking(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="booking_user")
    tour = models.ForeignKey(Destination, on_delete=models.SET_NULL,null=True, related_name="booking_tour")
    slots = models.IntegerField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    tour_time = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    booking_total = models.IntegerField(blank=True, null=True)  # Add this field
    discounted_total = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.booking_total = self.slots * self.tour.amount  # Calculate the booking total
        self.discounted_total = self.slots * (self.tour.amount - self.tour.discount)

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user) + str("-") + str(self.tour)
    
class Payment(models.Model):
    payment_choices = [
        ("M-PESA", "M-PESA"),
        ("Paypal", "Paypal"),
        ("Stripe", "Stripe")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, related_name="payment_booking")
    type_payment = models.CharField(max_length=200, choices=payment_choices, null=True, blank=True)
    reference_id = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now, null=True)

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
    payment_date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.invoice_id)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cart")
    booking = models.ManyToManyField(Booking, related_name="booking")
    created_date = models.DateTimeField(default=datetime.now, null=True)
    paid = models.BooleanField(default=False)
    cleared = models.BooleanField(default=False)

    #Keep count of items in cart
    def number_of_items(self):
        return self.booking.count()

    def __str__(self):
        return str(self.id)
    
    def createCart(sender, instance, created, **kwargs):
        if created:
            user_profile = Profile(user=instance)
            user_profile.save()

    post_save.connect(createCart, sender=User)



