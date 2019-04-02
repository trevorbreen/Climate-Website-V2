# Generated by Django 2.1.7 on 2019-03-21 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0004_auto_20190321_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='food_intake',
            field=models.DecimalField(choices=[(1.5, 'a lot more than other people my age'), (1.25, 'somewhat more than other people my age'), (1, 'about the same as other people my age'), (0.75, 'somewhat less than other people my age'), (0.5, 'a lot less than other people my age')], decimal_places=2, max_digits=3, verbose_name='What is the best way to describe the amount of food you eat?'),
        ),
    ]
