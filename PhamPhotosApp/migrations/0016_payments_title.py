# Generated by Django 3.1.5 on 2021-08-11 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhamPhotosApp', '0015_auto_20210811_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]