# Generated by Django 3.0.8 on 2021-08-08 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhamPhotosApp', '0007_auto_20210807_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='photo',
            field=models.ImageField(upload_to=''),
        ),
    ]
