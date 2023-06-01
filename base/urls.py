"""tours URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.Home, name="home"),
    path("contact/", views.Contact, name="contact"),
    path("excursion/", views.Excursions, name="excursions"),
    path("destination/<str:pk>/", views.destination_page, name="destination"),
    path("book/<str:pk>/", views.book_tour, name="book"),
    path("like/<str:pk>/", views.tour_like, name="like"),
    path("tour-update/<int:pk>/", views.tour_update, name="tour-update"),
    path("cart-update/<int:pk>/", views.cart_update, name="cart-update"),
    path("gallery/", views.Gallery, name="gallery"),
    path("mpesa/<int:pk>/", views.mpesa_payment, name="mpesa"),
    path("callback/", views.daraja_callback, name="mpesa-callback"),
    path("safari/", views.Safari, name="safari"),
    path("farm/", views.Farm, name="farm"),
    path("hikingadventure/", views.hikingAdventure, name="hikingadventure"),
    path("review/<str:pk>/", views.Review_tour, name="review"),
    path("checkout/<int:booking_id>/", views.checkout, name="checkout"),
    path("register/", views.Register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("cart/", views.cart, name="cart"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name='password_reset' ),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name='password_reset_done' ),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm' ),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete' ),
    path("payment/success/", views.payment_success, name="payment_success"),
    path("payment/cancel/", views.payment_cancel, name="payment_cancel"),
    path('charge/', views.charge, name='charge'),
    path('paypal-test/<int:pk>', views.create_payment, name='paypal-test'),
    path('paypal/execute_payment/', views.execute_payment, name='paypal-test/execute'),
    path('paypal/cancel_payment/', views.cancel_payment, name='paypal-test/cancel'),
    # path("update-cart/", views.update_cart, name="update_cart"),
    path("delete-tour/<int:pk>/", views.delete_tour, name="delete_tour"),
    path("delete-cart/<int:pk>/", views.delete_cart, name="delete_cart"),
    path("search-tour/", views.search_tour, name="search")
    
    # path('get_access_token/', views.get_access_token, name='get_access_token'),
    # path('get_payment_details/<str:payment_id>/', views.get_payment_details, name='get_payment_details'),

]
