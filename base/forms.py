from django.contrib.auth.forms import UserCreationForm
from .models import User
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
        

        