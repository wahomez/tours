from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import *
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
import paypalrestsdk
import requests
import json
import stripe
from .keys import *
from .mpesa import ac_token
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.http import JsonResponse, HttpResponseServerError, HttpResponseBadRequest
from datetime import datetime
from .utils import create_invoice_pdf
from requests.auth import HTTPBasicAuth
import base64




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
    try:
        payment = Payment.objects.get(booking=booking)
        payment_date = payment.date
        print(payment_date)
    except:
        print("Error in date")
    checkout = Booking.objects.filter(id=booking_id)
    price = booking.tour.amount
    people = booking.slots
    total = price*people
    booking = booking.id
    
    

    #invoice form data
    if request.method == "POST":
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]
        email = request.POST["email"]
        tour = request.POST["tour"]
        tour_date = request.POST["tourDate"]
        price = price
        slots = people
        total = total
        payment_date = payment_date
        invoice = Invoice.objects.create(first_name=first_name, last_name=last_name, email=email, tour=tour, tour_date=tour_date, price=price, slots=slots, total=total, payment_date=payment_date)
        invoice.save()
        messages.success(request, ("Successfully generated your invoice!"))
        return redirect("/")

        # #send the invoice to cutomer via email
        # pdf = create_invoice_pdf(invoice)
        # email = EmailMessage(
        #     subject='Invoice from Cruize Beyond and Travels',
        #     body='Please find attached your invoice from Cruize Beyond Travels',
        #     from_email=settings.EMAIL_HOST_USER,
        #     to=[invoice.email],
        #     cc=[settings.EMAIL_HOST_USER],
        # )
        # email.attach(filename='invoice.pdf', content=pdf.getvalue(), mimetype='application/pdf')
        # return HttpResponse("Invoice successfully sent to email")

    context = {
        "checkout" : checkout,
        "total" : total,
        'booking' : booking,
    }
    return render(request, "checkout.html", context)

def payment_success(request):
  return render(request, "payment_success.html")

def payment_cancel(request):
  return render(request, "payment_cancel.html")


def mpesa_payment(request, pk):
    booking = Booking.objects.get(id=pk)
    #get payment details from form
    if request.method == "POST":
        mobile = request.POST["mobile"]
        amount = request.POST["amount"]
        print("KEY:", pk)
        # order = Order.objects.get(order_id=pk)
        tour = booking.tour.name
        print("Tour:", tour)
        booking_id = booking.id
        print("ID:", booking_id)
    #get access token
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(auth_url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    access_token = response.json()["access_token"]

    #get payment details
    # mobile = 254748373873
    # amount = 100
    # description = "Product 1"

    #create payment payload
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % access_token
    }

    payload = {
        "BusinessShortCode": 174379,
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMwMzIwMjM1NTA2",
        "Timestamp": "20230320235506",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": "254" + mobile,
        "PartyB": 174379,
        "PhoneNumber": "254" + mobile,
        "CallBackURL": "https://cruizesafaris.com/mpesa-callback/",
        "AccountReference": "Cruize Beyond",
        "TransactionDesc": tour
    }
    #stk push api
    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, json = payload)
    
    code = response.json()
    print(code)

    try:
        if code["ResponseCode"] == '0':
            print("Complete pin prompt sent to your device to complete payment!")
            booking = Booking.objects.get(id=booking_id)
            payment = Payment.objects.create(user=booking.user, booking=booking)
            Booking.objects.update(paid=True)
            payment.save()
            messages.success(request, ("Payment successfull"))
            return redirect("mpesa-callback", booking_id)
        else:
            print("Failed transaction. Try again!")
    except:
        print("Code didn't work")
    # print("Token:", access_token)
    return HttpResponse("We are good")

def mpesa_callback(request, pk):
    booking = Booking.objects.get(id=pk)
    tour = booking.tour
    print(tour)
    if request.method == 'POST':
        # Extract payment details from the request
        transaction_reference = request.POST.get('TransactionReference')
        amount = request.POST.get('Amount')
        tour = request.POST.get("TransactionDesc")
        # Validate the payment
        print("Amount:", amount)
        print("Reference:", transaction_reference)
        # Update your application's records
        # ...
        # Return a response to Mpesa
        return HttpResponse('OK')
    else:
        return HttpResponseBadRequest('Invalid request method')


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

def create_payment(request, pk):
    paypalrestsdk.configure(
        client_id= CLIENT_ID,
        client_secret= CLIENT_SECRET,
        mode= "sandbox"
    )
    booking = Booking.objects.get(id=pk)
    tour = booking.tour.name
    price = booking.tour.amount
    people = booking.slots
    total = price*people
    booking_id = booking.id
    if booking.paid == True:
        messages.success(request, ("Your tour is already paid for!"))
        return redirect("checkout", pk)
    else:
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/paypal/execute_payment/",
                "cancel_url": "http://localhost:8000/paypal/cancel_payment/"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": tour,
                        "sku": booking_id,
                        "price": price,
                        "currency": "USD",
                        "quantity": people
                    }]
                },
                "amount": {
                    "total": total,
                    "currency": "USD"
                },
                "description": "Transaction description.",
                "custom": booking_id
            }]
        })
        if payment.create():
            for link in payment.links:
                if link.rel == 'approval_url':
                    return redirect(link.href)
        else:
            return HttpResponseServerError
    
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    
    payment = paypalrestsdk.Payment.find(payment_id)
    booking_id = payment.transactions[0].custom
    print(booking_id)
    if payment.execute({"payer_id": payer_id}):
        booking = Booking.objects.get(id=booking_id)
        payment = Payment.objects.create(user=booking.user, booking=booking)
        Booking.objects.update(paid=True)
        payment.save()
        return redirect("checkout", booking_id)

        # Payment successful, do something here
        # return HttpResponse("Payment worked")
    else:
        # Payment unsuccessful, do something here
        return HttpResponse("Payment failed")

def cancel_payment(request):
    return HttpResponse("Payment cancelled")


