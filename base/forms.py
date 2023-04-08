from django.contrib.auth.forms import UserCreationForm
from .models import User, Booking
from django import forms

#Create forms
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email","username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class TourForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("tour", "start_date", "end_date", "tour_time")

        widgets = {
            "tour" : forms.Select(attrs={"class":"form-select"}),
            "start_date" : forms.TextInput(attrs={"class":"form-control", "type":"date"}),
            "end_date" : forms.TextInput(attrs={"class":"form-control", "type":"date"}),
            "tour_time" : forms.TextInput(attrs={"class":"form-control"}),
        }

class TourForm_1(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("tour", "start_date", "tour_time")

        widgets = {
            "tour" : forms.Select(attrs={"class":"form-select"}),
            "start_date" : forms.TextInput(attrs={"class":"form-control", "type":"date"}),
            "tour_time" : forms.TextInput(attrs={"class":"form-control"}),
        }
        

        