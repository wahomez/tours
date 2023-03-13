# Generated by Django 4.1.5 on 2023-03-13 20:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_remove_payment_tour_payment_booking_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoice_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('tour_date', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('slots', models.IntegerField()),
                ('total', models.IntegerField()),
                ('payment_date', models.DateTimeField()),
                ('tour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.destination')),
            ],
        ),
    ]