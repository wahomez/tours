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
# from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.http import JsonResponse, HttpResponseServerError, HttpResponseBadRequest
from datetime import datetime
# from .utils import create_invoice_pdf
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth
import base64
from google_currency import convert
from .forms import TourForm, TourForm_1




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
            else:
                messages.success(request, ("There was an error with your form, Kindly fill again!"))
                return redirect("/")
        else:
            messages.success(request, ("There was an error with your form, Kindly fill again!"))
            return redirect("/")
    else:

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
    review = Review.objects.filter(tour=pk)
    duration = destination.duration
    print("Duration:", duration)
    # booking = Booking.objects.get(tour=pk, user=request.user)
    # slots = booking.slots
    # print("Booking:", slots)
   
    if request.method == "POST":
        slots = request.POST['slots']
        tour_time = request.POST['tour-time']
        
        tour = destination
        if duration == 1:
            start_date = request.POST['start-date']
            end_date = None
        else:
            start_date = request.POST['start-date']
            end_date = request.POST['end-date']
            
        booking = Booking.objects.create(user=request.user, tour=tour, slots=slots, start_date=start_date, end_date=end_date, tour_time=tour_time)
        booking.save()
        messages.success(request, "You have booked a tour successfully. Proceed to checkout!")
        return redirect("checkout", booking_id=booking.id)

    context = {
        "tours" : tours,
        "review" : review,
        
    }
    return render(request, "destination.html", context)

def Gallery(request):
    return render(request, "gallery.html")

def Safari(request):
    tours = Destination.objects.filter(category="Safari Tours")
    context = {
        "tours" : tours
    }
    return render(request, "safaritours.html", context)

def Farm(request):
    tours = Destination.objects.filter(category="Farm Tours")
    context = {
        "tours" : tours
    }
    return render(request, "farmtours.html", context)

def hikingAdventure(request):
    tours = Destination.objects.filter(category="Hiking and Adventures Tours")
    context = {
        "tours" : tours
    }
    return render(request, "hikingadventuretours.html", context)


def Review_tour(request, pk):
    tour = Destination.objects.get(id=pk)
    print("Toour: ", tour)
    tour_review = Review.objects.all
    if request.method == 'POST':
        user = request.user
        tour = tour
        comment = request.POST['comment']
        tour_review = Review.objects.create(user=user,tour=tour, comment=comment)
        tour_review.save()
        messages.success(request, ("Review sent successfully"))
        return redirect("destination", pk )
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
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Registration was successful!")
            return redirect("/")
        else:
            messages.success(request, ("There was an error when login in!"))
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
            return redirect("/")

    else:
        return render(request, "login.html")

def logout_user(request):
    logout(request)
    messages.success(request, ("You have successfully logged out"))
    return redirect("/")

def tour_update(request, pk):
    booking = Booking.objects.get(id=pk)
    duration = booking.tour.duration
    print("Dur:", duration)
    if request.method == "POST":
        form = TourForm(request.POST, instance=booking)
        print("Sth is happening")
        if form.is_valid():
            form.save(commit=False)
            form.save()
            messages.success(request, ("You have successfully updated the tour details!"))
            return redirect("checkout", pk)
        else:
            messages.success(request, ("There was an error when updating your tour details. Kindly try again!"))
            return redirect("checkout", pk)
    print("Maybe woking")
    return redirect("checkout", pk)


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
    discount = booking.tour.discount
    discounted_total = price-discount
    people = booking.slots
    total = discounted_total*people
    json_string = convert('usd', 'kes', total)
    convert_total = json.loads(json_string)
    converted_total = convert_total["amount"]
    payment_date = None

    duration = booking.tour.duration
    # print("Tour:", tour)

    if duration == 1:
        form = TourForm_1(instance=booking)
    else:
        form = TourForm(instance=booking)
    
    # total = convert_total["amount"]
    
    booking = booking.id
    # print("Final dict: ", convert_total)
    # print("Final price: ", final_total)
    

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
        messages.success(request, ("Successfully completed checkout.Your invoice will be sent to your email shortly."))
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
        "converted_total" : converted_total,
        "form" : form
        }
    return render(request, "checkout.html", context)

def payment_success(request):
  return render(request, "payment_success.html")

def payment_cancel(request):
  return render(request, "payment_cancel.html")


def mpesa_payment(request, pk):
    booking = Booking.objects.get(id=pk)
    #get payment details from form
    if booking.paid == True:
        messages.success(request, ("Your tour is already paid for!"))
        return redirect("checkout", pk)
    else:
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
            "CallBackURL": "https://cruizesafaris.com/callback/",
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
                messages.success(request, ("Payment request was sent successfully!"))
                return redirect("checkout", booking_id)
            else:
                print("Failed transaction. Try again!")
        except:
            print("Code didn't work")
        # print("Token:", access_token)
        return HttpResponse("We are good")

@csrf_exempt
def daraja_callback(request):
    print("Working!")
    # Extract relevant data from the callback
    transaction_id = request.POST.get('TransID', '')
    transaction_status = request.POST.get('TransStatus', '')

    try:
        if request.method == 'POST':
            # Retrieve the JSON data from the request body
            callback_data = json.loads(request.body)

            # Check if the transaction was successful
            if callback_data.get('Body.stkCallback.ResultCode') == '0':
                # Handle the successful transaction
                print("Callback Data:", callback_data)
                messages.success(request, ("Payment was successfull. Complete Checkout!"))

                # Return a success response
                response_data = {
                    'ResultCode': 0,
                    'ResultDesc': 'Success'
                }
                return HttpResponse(json.dumps(response_data), content_type='application/json')
            else:
                # Handle the failed transaction
                # ...
                messages.success(request, ("Payment was not successfull. Try again!"))
                print("Payment Cancelled!")

                # Return an error response
                response_data = {
                    'ResultCode': 1,
                    'ResultDesc': 'Error'
                }
                return HttpResponse(json.dumps(response_data), content_type='application/json')

        # Return a bad request response if the request method is not POST
        response_data = {
            'ResultCode': 1,
            'ResultDesc': 'Invalid request method'
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
    except:
        print("Error!")

    # Perform any necessary actions, such as updating your database
    # ...

    # Return a response to Daraja
    return HttpResponse(status=200)


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
        reference_id = payment_id
        type_payment = "Paypal"
        booking = Booking.objects.get(id=booking_id)
        payment = Payment.objects.create(user=booking.user, booking=booking, reference_id=reference_id, type_payment=type_payment)
        Booking.objects.update(paid=True)
        payment.save()
        messages.success(request, ("Payment was successfull. Completed Checkout!"))
        return redirect("checkout", booking_id)

        # Payment successful, do something here
        # return HttpResponse("Payment worked")
    else:
        # Payment unsuccessful, do something here
        messages.success(request, ("Payment not successfull try again"))
        return redirect("checkout", booking_id)

def cancel_payment(request):
    messages.success(request, ("Payment not successfull try again"))
    return redirect("checkout")


