# Generated by Django 3.0.8 on 2021-07-28 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PhamPhotosApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='role',
        ),
    ]