# Generated by Django 3.1.5 on 2021-08-11 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhamPhotosApp', '0014_auto_20210811_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='tokens',
            field=models.FloatField(default=0),
        ),
    ]
