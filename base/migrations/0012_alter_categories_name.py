# Generated by Django 4.1.5 on 2023-03-09 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_remove_categories_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='name',
            field=models.CharField(choices=[('Excursions', 'Excursions'), ('Safari Tours', 'Safari Tours'), ('Farm Tours', 'Farm Tours'), ('Hiking and Adventures Tours', 'Hiking and Adventures Tours')], max_length=50),
        ),
    ]
