from django.contrib.auth.forms import UserCreationForm
from .models import User, Booking
from django import forms

#Create forms
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="What's your email?", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    class Meta:
        model = User
        fields = ("email","username", "password1", "password2")
        

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # self.fields['email'].widget.attrs['class'] = 'form-control'
        # self.fields['email'].widget.attrs['placeholder'] = 'Email address'
        # self.fields['email'].label = "What's your email?"
        # self.fields['email'].help_text = "<span class='form-text text-muted'>We will never share your email with anyone else.</span>"

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = "What should we call you?"
        # self.fields['username'].help_text = "<span class='form-text text-muted'>We will never share your email with anyone else.</span>"

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = "Create your magical password"
        # self.fields['password1'].help_text = "<span class='form-text text-muted'>The password shouldn't be similar to email or username</span>"

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = "Confirm your magical password"
        # self.fields['password2'].help_text = "<span class='form-text text-muted'>The 2 password didn't match </span>"

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
        

        