from django.contrib import admin
from .models import users, purchases, photos, payments, videos, videopurchases
from django.contrib import messages
from django.utils.translation import ngettext

# Register your models here.
admin.site.site_header = 'UI Administrator'





def approve(modeladmin, request, queryset):
    for image in queryset:
        image.approved = True
        image.save()
approve.short_description = 'Quickly Accept Images'




class modphotos(admin.ModelAdmin):
    list_display = ['photo', 'approved', 'price']
    actions = [approve,]  # <-- Add the list action function here



class modpurchases(admin.ModelAdmin):
    list_display = ['User', 'Photo', 'date','paied']
   

class modpayments(admin.ModelAdmin):
    list_display = ['user', 'amount', 'added']


class modusers(admin.ModelAdmin):
    list_display = ['user', 'tokens']


class modpurchasess(admin.ModelAdmin):
    list_display = ['User', 'video', 'date','paied']


class modphotoss(admin.ModelAdmin):
    list_display = ['video', 'approved', 'price']
    actions = [approve,]  # <-- Add the list action function here



    


admin.site.register(photos, modphotos)
admin.site.register(purchases,modpurchases)
admin.site.register(users, modusers)
admin.site.register(payments, modpayments)
admin.site.register(videos,modphotoss)
admin.site.register(videopurchases,modpurchasess)