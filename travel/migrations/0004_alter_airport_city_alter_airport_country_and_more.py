# Generated by Django 4.1 on 2022-10-27 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_airport_booking_flight_user_nationality_user_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airport',
            name='city',
            field=models.CharField(default='none', max_length=32),
        ),
        migrations.AlterField(
            model_name='airport',
            name='country',
            field=models.CharField(default='none', max_length=32),
        ),
        migrations.AlterField(
            model_name='airport',
            name='name',
            field=models.CharField(default='none', max_length=128),
        ),
    ]
