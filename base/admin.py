from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile, Tour, Trip, Review, User

#Unregister Groups
admin.site.unregister(Group)

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Tour)
admin.site.register(Trip)
admin.site.register(Review)