# Generated by Django 5.0.6 on 2024-11-08 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='', verbose_name='picture'),
        ),
    ]