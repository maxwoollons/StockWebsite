# Generated by Django 3.1.5 on 2021-08-11 10:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PhamPhotosApp', '0013_payment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='payment',
            new_name='payments',
        ),
    ]
