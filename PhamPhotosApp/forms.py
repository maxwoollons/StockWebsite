from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ValidationError
from .models import photos, videos, exchange
from PIL import Image



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    confirm = forms.BooleanField(required=True, label="I accept the terms and conditions")
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2','confirm']
       
        
        
        
class MediaSubmit(ModelForm):
    class Meta:
        model = photos
        exclude = ('owner','approved','price')
        



class VideoSubmit(ModelForm):
    class Meta:
        model = videos
        exclude = ('owner','approved','price')



class ExchangeSubmit(ModelForm):
    class Meta:
        model = exchange
        fields = ('amount','paypal')
        labels = {
            "amount": "Amount to withdraw ($AUD)",
            "paypal": "Paypal Email",
        }
        

                