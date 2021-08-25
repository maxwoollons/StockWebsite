from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT, SET_NULL
from django.db.models.fields import BooleanField, CharField, DateTimeField, IntegerField, TextField
import datetime
from django.contrib.auth.models import User

from django.db.models.fields.related import ForeignKey, ManyToManyField


from .validators import file_size
from PIL import *
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, SmartResize
from .processors import Watermark
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True





CHOICES = (
            ('Animals and Wild Life', 'Animals and Wild Life'),  
            ('Arts', 'Arts'),
            ('Business & Professions', 'Business & Professions'),
            ('Coronavirus/ Pandemic', 'Coronavirus/ Pandemic'),
            ('Education', 'Education'),
            ('Elements of Nature', 'Elements of Nature'),
            ('Food', 'Food'),
            ('Green Planet', 'Green Planet'),
            ('Home', 'Home'),
            ('Industry', 'Industry'),
            ('Lifestyle', 'Lifestyle'),
            ('Love', 'Love'),
            ('Landscapes', 'Landscapes'),
            ('Medical & Health', 'Medical & Health'),
            ('People', 'People'),
            ('Religion & Traditions', 'Religion & Traditions'),
            ('Sport & Fitness', 'Sport & Fitness'),
            ('Technology & Science', 'Technology & Science'),
            ('Motion or Time Lapse','Motion or Time Lapse'),
            ('Travel & World', 'Travel & World'),
            ('Transportation', 'Transportation'),
            ('Urban & City', 'Urban & City'),
            ('Vintage', 'Vintage'),

)

CHOICES_FORMAT = (
            ('4K (UHD)', '4K (UHD)'),
            ('2K', '2K'),
            ('1080p (FHD)', '1080p (FHD)'),  
          

)



class users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tokens = models.IntegerField(default=0)
    def __str__(self):
        return str(self.id) + str(self.user) + str(self.tokens) 




class photos(models.Model): #PHOTO
    photo = models.ImageField(null=False, blank=False, upload_to="images/")  
    price = models.IntegerField()
    title = models.CharField(max_length=255)
    added = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=CASCADE)
    category = models.CharField(max_length=255, choices=CHOICES)
    cameratype = models.CharField(max_length=255, null=True, blank=True)
    approved = models.BooleanField(default=False)
    image_thumbnail = ImageSpecField(source="photo",processors=[ResizeToFill(800,800)],format="JPEG",options={'quality':30})
    large_image_thumbnail = ImageSpecField(source="photo",format="JPEG",options={'quality':60}, processors=[Watermark()])
    def __str__(self):
        return str(self.id) + ' Approved:' + str(self.approved)

    
    
    
class purchases(models.Model):
    User = models.ForeignKey(users, on_delete=CASCADE)
    Photo = models.ForeignKey(photos, on_delete=CASCADE)
    date = models.DateTimeField(auto_now=True)
    downloaded = models.BooleanField()
    paied = models.FloatField(null=True, blank=True)
    def __str__(self):
        return str(self.id) +  ' ' + str(self.User)
    
    
class cart(models.Model):
    photo = ForeignKey(photos, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)

class payments(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    amount = models.FloatField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    added = models.DateTimeField(auto_now=True)


class creditpurchases(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    creditamount = models.FloatField(null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    added = models.DateTimeField(auto_now=True)



class videos(models.Model): #PHOTO
    video = models.FileField(null=False, blank=False, upload_to="videos/", validators=[file_size])  
    price = models.IntegerField()
    title = models.CharField(max_length=255)
    added = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=CASCADE)
    category = models.CharField(max_length=255, choices=CHOICES)
    format = models.CharField(max_length=255, choices=CHOICES_FORMAT)
    cameratype = models.CharField(max_length=255, null=True, blank=True)
    approved = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id) + ' Approved:' + str(self.approved)


class videopurchases(models.Model):
    User = models.ForeignKey(users, on_delete=CASCADE)
    video = models.ForeignKey(videos, on_delete=CASCADE)
    date = models.DateTimeField(auto_now=True)
    downloaded = models.BooleanField()
    paied = models.FloatField(null=True, blank=True)
    def __str__(self):
        return str(self.id) +  ' ' + str(self.User)
    
    
    
    
class exchange(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    amount = models.IntegerField(null=False,blank=False)
    paypal = models.EmailField(null=False,blank=False)
    time = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    
    
class savedphoto(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    image = models.ForeignKey(photos, on_delete=CASCADE)
    
class savedvideo(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    image = models.ForeignKey(videos, on_delete=CASCADE)
    

   





