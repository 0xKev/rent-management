# Generated by Django 5.0.3 on 2024-03-25 04:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent_management', '0005_alter_rental_lease_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='lease_end_date',
            field=models.DateField(default=datetime.datetime(2024, 4, 24, 4, 50, 42, 410290, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='rental',
            name='lease_start_date',
            field=models.DateField(default=datetime.datetime(2024, 3, 25, 4, 50, 42, 410290, tzinfo=datetime.timezone.utc)),
        ),
    ]
