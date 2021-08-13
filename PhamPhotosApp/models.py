from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT, SET_NULL
from django.db.models.fields import BooleanField, CharField, DateTimeField, IntegerField, TextField
import datetime
from django.contrib.auth.models import User

from django.db.models.fields.related import ForeignKey, ManyToManyField

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, SmartResize

from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True


class users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tokens = models.FloatField(default=0)
    def __str__(self):
        return str(self.id) + str(self.user) + str(self.tokens) 




class photos(models.Model): #PHOTO
    photo = models.ImageField(null=False, blank=False, upload_to="images/")  
    price = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    added = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=CASCADE)
    cameratype = models.CharField(max_length=255, null=True, blank=True)
    approved = models.BooleanField(default=False)
    image_thumbnail = ImageSpecField(source="photo",processors=[ResizeToFill(800,800)],format="JPEG",options={'quality':60})
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






