# Generated by Django 4.1.5 on 2023-03-09 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_booking_categories_payment_remove_trip_tour_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='image',
        ),
    ]