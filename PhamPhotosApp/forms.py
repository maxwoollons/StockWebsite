from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ValidationError
from .models import photos, videos
from PIL import Image



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
        
        
        
        
class MediaSubmit(ModelForm):
    class Meta:
        model = photos
        exclude = ('owner','approved')



class VideoSubmit(ModelForm):
    class Meta:
        model = videos
        exclude = ('owner','approved')

                