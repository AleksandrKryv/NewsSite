from django import forms
from django.forms import ModelForm
from .models import *


class NSuserForm(ModelForm):
    class Meta:
        model = NSuser
        fields = ('username', 'password', 'email', 'phone_number')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                               "Enter username"}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':
                                                   "Enter password with at least 8 digits"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':
                                             "Enter your email"
                                             }),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                   "Enter your phone number"
                                                   }),


        }

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if NSuser.objects.filter(phone_number=data):
            raise forms.ValidationError("Phone number already exists")
        return data


class NSuserCabinetForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control square', 'placeholder':
                                                                             "Username"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control square', 'placeholder':
                                                                           "Email"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control square', 'placeholder':
                                                                                 "phone number"}))
    photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={}))

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if NSuser.objects.filter(phone_number=data):
            raise forms.ValidationError("Phone number already exists")

    def clean_username(self):
        data = self.cleaned_data['username']
        if NSuser.objects.filter(username=data):
            raise forms.ValidationError("User with this username already exists")

    def clean_email(self):
        data = self.cleaned_data['email']
        if NSuser.objects.filter(email=data):
            raise forms.ValidationError("User with this email already exists")


class LoginForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':
                                                                 "Enter password with at least 8 digits"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                             "Enter your username"}))

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

    def clean_username(self):
        username = self.cleaned_data['username']
        return username
