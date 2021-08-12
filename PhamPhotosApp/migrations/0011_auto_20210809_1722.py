# Generated by Django 3.0.8 on 2021-08-09 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhamPhotosApp', '0010_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='photos',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='photos',
            name='cameratype',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]