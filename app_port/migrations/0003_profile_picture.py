# Generated by Django 2.1.7 on 2019-04-04 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_port', '0002_channel_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, upload_to='profile_pictures'),
        ),
    ]
