# Generated by Django 2.1.7 on 2019-05-22 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0017_auto_20190522_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='sex',
        ),
    ]