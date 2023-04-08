# Generated by Django 4.1.7 on 2023-04-02 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_booking_tour_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='tour_time',
        ),
        migrations.AddField(
            model_name='destination',
            name='tour_time',
            field=models.CharField(blank=True, choices=[('06.30 a.m. - 09.30 a.m.', '06.30 a.m. - 09.30 a.m.'), ('10.30 a.m. - 12.30 a.m.', '10.30 a.m. - 12.30 a.m.'), ('12.30 p.m. - 02.30 p.m.', '12.30 a.m. - 2.30 p.m.')], max_length=200, null=True),
        ),
    ]