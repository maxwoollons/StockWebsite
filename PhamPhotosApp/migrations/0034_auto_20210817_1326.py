# Generated by Django 3.0.8 on 2021-08-17 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PhamPhotosApp', '0033_auto_20210817_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedvideo',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PhamPhotosApp.videos'),
        ),
    ]
