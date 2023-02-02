from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from .models import *
from django.core.mail import send_mail

# Create your views here.
def Home(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            user = authenticate(request, email=user.email, password=request.POST['password1'])
            if user is not None:
                login(request, user)
                messages.success(request, ("You are logged in successfully"))
                return redirect("/")

    context = {
        "form" : form
    }
    return render(request, 'index.html', context)

def Contact(request):
    if request.method == 'POST':
        Email = request.POST['userEmail']
        Name = request.POST['userName']
        Message = request.POST['userMessage']

        #send mail
        send_mail(
            "Email from contact form by "+ Name,
            "The message was as follows:" + Message + ". You can get in touch via the following email -" + Email,
            "wahome4jeff@gmail.com",
            ["info@cruizebeyond.co.ke"]
        )
        messages.success(request, ("Contact form sent successfully"))
        return redirect("/")
        

    return render(request, "contactus.html")

def Excursions(request):
    return render(request, "excursions.html")

def Gallery(request):
    return render(request, "gallery.html")

def Safari(request):
    return render(request, "safaritours.html")


def Review_tour(request):
    tour_review = Review.objects.all()
    if request.method == 'POST':
        user = request.user
        comment = request.POST['comment']
        tour_review = Review.objects.create(user=user, comment=comment)
        tour_review.save()
        messages.success(request, ("Review sent successfully"))
        return redirect("/")
    else:
        messages.success(request, ("Couldn't send review"))

    return HttpResponse("It works")

def Register(request):
    if request.method =="POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        form = User.objects.create(email = email, username=username, password=password)
        form.save()
        messages.success(request, "Registration was successful!")
        return redirect("/")

    else:       
        context = {
            "form":form
        }
        return render(request, "register.html", context)

def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You are logged in successfully"))
            return redirect("/")
        else:
            messages.success(request, ("There was an error when login in!"))

    else:
        return render(request, "login.html")

def logout_user(request):
    logout(request)
    messages.success(request, ("You have successfully logged out"))
    return redirect("/")
