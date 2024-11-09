# Generated by Django 5.0.6 on 2024-11-08 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_userprofile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(default=18),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(default='Male', max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='status',
            field=models.CharField(default='Active', max_length=100),
        ),
    ]
