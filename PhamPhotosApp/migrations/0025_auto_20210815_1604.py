# Generated by Django 3.1.5 on 2021-08-15 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhamPhotosApp', '0024_auto_20210815_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='category',
            field=models.CharField(choices=[('Animals and Wild Life', 'Animals and Wild Life'), ('Arts', 'Arts'), ('Business & Professions', 'Business & Professions'), ('Coronavirus/ Pandemic', 'Coronavirus/ Pandemic'), ('Education', 'Education'), ('Elements of Nature', 'Elements of Nature'), ('Food', 'Food'), ('Green Planet', 'Green Planet'), ('Home', 'Home'), ('Industry', 'Industry'), ('Lifestyle', 'Lifestyle'), ('Love', 'Love'), ('Landscapes', 'Landscapes'), ('Medical & Health', 'Medical & Health'), ('People', 'People'), ('Religion & Traditions', 'Religion & Traditions'), ('Sport & Fitness', 'Sport & Fitness'), ('Technology & Science', 'Technology & Science'), ('Motion or Time Lapse', 'Motion or Time Lapse'), ('Travel & World', 'Travel & World'), ('Transportation', 'Transportation'), ('Urban & City', 'Urban & City'), ('Vintage', 'Vintage')], max_length=255),
        ),
        migrations.AlterField(
            model_name='videos',
            name='category',
            field=models.CharField(choices=[('Animals and Wild Life', 'Animals and Wild Life'), ('Arts', 'Arts'), ('Business & Professions', 'Business & Professions'), ('Coronavirus/ Pandemic', 'Coronavirus/ Pandemic'), ('Education', 'Education'), ('Elements of Nature', 'Elements of Nature'), ('Food', 'Food'), ('Green Planet', 'Green Planet'), ('Home', 'Home'), ('Industry', 'Industry'), ('Lifestyle', 'Lifestyle'), ('Love', 'Love'), ('Landscapes', 'Landscapes'), ('Medical & Health', 'Medical & Health'), ('People', 'People'), ('Religion & Traditions', 'Religion & Traditions'), ('Sport & Fitness', 'Sport & Fitness'), ('Technology & Science', 'Technology & Science'), ('Motion or Time Lapse', 'Motion or Time Lapse'), ('Travel & World', 'Travel & World'), ('Transportation', 'Transportation'), ('Urban & City', 'Urban & City'), ('Vintage', 'Vintage')], max_length=255),
        ),
    ]
