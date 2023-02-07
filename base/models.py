from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.db.models.signals import post_save

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

class Tour(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    amount = models.IntegerField()
    poster = models.ImageField()
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    deadline_date = models.DateTimeField()

    def __str__(self):
        return str(self.name)+ ('----') + str(self.location)

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trip_user')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="trip_tour")
    paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.tour) + ('----') + str(self.user.username)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review")
    comment = models.TextField()
    uploaded_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Destination(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    about = models.TextField()
    notes = models.TextField()
    schedule = models.TextField()
    itinerary = models.TextField()
    poster = models.ImageField()

    def __str__(self):
        return self.name



