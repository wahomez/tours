from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import *
from django.core.mail import send_mail
from django.urls import reverse
import paypalrestsdk
import requests
import json
import stripe
from .keys import *
from .mpesa import ac_token


stripe.api_key = STRIPE_SECRET_KEY


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
    tours = Destination.objects.filter(category="Excursions")
    context = {
        "tours" : tours
    }
    return render(request, "excursions.html", context)

def destination_page(request, pk):
    tours = Destination.objects.filter(id=pk)
    destination = Destination.objects.get(id=pk)
    review = Review.objects.filter(destination_review=pk)
    booking = Booking.objects.all()
   



    if request.method == "POST":
        slots = request.POST['slots']
        tour = destination
        booking = Booking.objects.create(user=request.user, tour=tour, slots=slots)
        booking.save()
        messages.success(request, "You have booked a tour successfully. Proceed to checkout!")
        return redirect("checkout", booking_id=booking.id)

    context = {
        "tours" : tours,
        "review" : review
    }
    return render(request, "destination.html", context)

def Gallery(request):
    return render(request, "gallery.html")

def Safari(request):
    return render(request, "safaritours.html")

def Farm(request):
    return render(request, "farmtours.html")

def hikingAdventure(request):
    return render(request, "hikingadventuretours.html")


def Review_tour(request):
    tour_review = Review.objects.all
    if request.method == 'POST':
        user = request.user
        comment = request.POST['comment']
        tour_review = Review.objects.create(user=user, comment=comment)
        tour_review.save()
        messages.success(request, ("Review sent successfully"))
        return redirect("/")
    else:

        context = {
            "review" : tour_review
        }
        return render(request, "review.html", context)


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

def checkout(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    checkout = Booking.objects.filter(id=booking_id)
    price = booking.tour.amount
    people = booking.slots
    total = price*people
    context = {
        "checkout" : checkout,
        "total" : total,
    }
    return render(request, "checkout.html", context)

def mpesa_payment(request):
        pay=Payment.objects.all()
        if request.method == "POST":
            Number = request.POST['number']
            Amount = request.POST['amount']
    #Mpesa API
        token = ac_token()
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' %token
        }
        payload = {
            "BusinessShortCode": 174379,
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMwMTA5MTI1NjU1",
            "Timestamp": "20230109125655",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": Amount,
            "PartyA": "254" + Number,
            "PartyB": 174379,
            "PhoneNumber": "254" + Number,
            "CallBackURL": 'https://api.darajambili.com/express-payment',
            "AccountReference": "Cruizesafari",
            "TransactionDesc": "Payment of X"
        }

        response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, json = payload)
        # print(response.text.encode('utf8'))
        code = response.json()
        try:
            if code['ResponseCode'] == '0':
                print("Successful!. Complete the pin prompt sent to your device")
                # payment = Payment.objects.update(Successful=True)
                # payment.save()
            else:
                print("Failed! Kindly try again.")
        except:
            'Message didnt work'
        # return code()

        messages.success(request, ("Your payment request has been sent successful!"))
        return redirect('/')

# paypalrestsdk.configure({
#   "mode": "sandbox", # Set to "live" for production
#   "client_id": "AZHgbmEC5kf3RMcOiO94d5QSq7NYgVeb8NhwMbbR2qBgsWUwX2752zKv8FZYgxcpp7AncFVtBabEdXHh",
#   "client_secret": "EDokXmFS6BnIJRBrGrVbBU5ZbK3Xs4J6K8PtgFDk5zfqqu7Vc0cHB_8Zx7WkJTcK4q5KCCUvO_Tjp60J"
# })

# Get payment details
# payment_id = "your_payment_id"




def payment_execute(request):
    return HttpResponse("It worked")
#   payment_id = request.GET.get("paymentId")
#   print(payment_id)
#   payer_id = request.GET.get("PayerID")
#   print(payer_id)
  
#   client_id = "AZHgbmEC5kf3RMcOiO94d5QSq7NYgVeb8NhwMbbR2qBgsWUwX2752zKv8FZYgxcpp7AncFVtBabEdXHh"
#   secret = "EDokXmFS6BnIJRBrGrVbBU5ZbK3Xs4J6K8PtgFDk5zfqqu7Vc0cHB_8Zx7WkJTcK4q5KCCUvO_Tjp60J"
    
#   access_token = get_access_token(client_id, secret)
    
#   payment_details = get_payment_details(access_token, payment_id)
     
#     # execute the payment
#   if 'links' in payment_details:
#     execute_payment_url = payment_details['links'][1]['href']
#     # continue with processing payment details
#   else:
#       pass
#     # handle the error
# #   execute_payment_url = payment_details["links"][1]["href"]
#   execute_payment_data = {
#         "payer_id": payer_id
#     }
#   execute_payment_response = requests.post(execute_payment_url, data=json.dumps(execute_payment_data),
#                                              headers={
#                                                  "Content-Type": "application/json",
#                                                  "Authorization": f"Bearer {access_token}"
#                                              })
#   execute_payment_response_json = execute_payment_response.json()
    
#     # check if payment was successful
#   if execute_payment_response.status_code == 200:
#         return HttpResponse("Payment was successful!")
#   else:
#         error_message = execute_payment_response_json.get("message", "Unknown error")
#         return HttpResponse(f"Payment failed: {error_message}")

# def get_access_token(client_id, secret):
#     url = "https://api.sandbox.paypal.com/v1/oauth2/token"
#     response = requests.post(url, auth=(client_id, secret), data={"grant_type": "client_credentials"})
#     response_json = response.json()
#     return response_json["access_token"]

# def get_payment_details(access_token, payment_id):
#     url = f"https://api.sandbox.paypal.com/v1/payments/payment/{payment_id}"
#     response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
#     response_json = response.json()
#     return response_json

#   payment = paypalrestsdk.Payment.find(payment_id)

#   if payment.execute({"payer_id": payer_id}):
#     # Save the payment details to your database
#     return redirect(reverse("payment_success"))
#   else:
#     return redirect(reverse("payment_cancel"))

def payment_success(request):
  return render(request, "payment_success.html")

def payment_cancel(request):
  return render(request, "payment_cancel.html")


def charge(request):
    if request.method == 'POST':
        token = request.POST['stripeToken']
        print("Processing")
        charge = stripe.Charge.create(
            amount = 0.01,
            currency = 'USD',
            description = 'Payment for Cruize Safaris',
            source=token
        )

        return redirect('success')
    
    return render(request, 'checkout.html', {'publishable_key': STRIPE_PUBLIC_KEY})

