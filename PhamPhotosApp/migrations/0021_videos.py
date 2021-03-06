# Generated by Django 3.1.5 on 2021-08-14 05:48

import PhamPhotosApp.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PhamPhotosApp', '0020_auto_20210813_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='videos/', validators=[PhamPhotosApp.validators.file_size])),
                ('price', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('added', models.DateTimeField(auto_now=True)),
                ('cameratype', models.CharField(blank=True, max_length=255, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
