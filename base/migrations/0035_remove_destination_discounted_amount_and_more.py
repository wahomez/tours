# Generated by Django 4.1.7 on 2023-05-11 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0034_destination_discounted_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination',
            name='discounted_amount',
        ),
        migrations.AddField(
            model_name='booking',
            name='discounted_total',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]