# Generated by Django 3.1.5 on 2021-08-13 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhamPhotosApp', '0019_creditpurchases_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='tokens',
            field=models.IntegerField(default=0),
        ),
    ]
