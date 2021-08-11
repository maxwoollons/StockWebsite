from django.contrib import admin
from .models import users, purchases, photos


# Register your models here.
admin.site.site_header = 'UI Administrator'

admin.site.register(photos)
admin.site.register(purchases)
admin.site.register(users)