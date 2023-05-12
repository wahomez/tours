from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile, Destination, User, Booking, Payment, Review, Invoice, Cart

#Unregister Groups
admin.site.unregister(Group)

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Destination)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Payment)
admin.site.register(Invoice)
admin.site.register(Cart)