from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ValidationError
from .models import photos
from PIL import Image



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
        
        
        
class MediaSubmit(ModelForm):
    class Meta:
        model = photos
        exclude = ('owner','approved')

            
        
    
                