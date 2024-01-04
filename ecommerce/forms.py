from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
class CustomUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter UserName'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email'}))
    password1=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Password'}))
    password2=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter confirm password'}))
    model=User
    fields=["username","email","password1","password2"]
