# Generated by Django 3.1.5 on 2021-08-11 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhamPhotosApp', '0011_auto_20210809_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='paied',
            field=models.FloatField(blank=True, null=True),
        ),
    ]