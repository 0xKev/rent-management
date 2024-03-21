# Generated by Django 5.0.3 on 2024-03-20 20:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent_management', '0005_alter_address_line2_alter_rental_lease_end_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='rent',
            new_name='default_rent',
        ),
        migrations.AddField(
            model_name='rental',
            name='rental_freq',
            field=models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annually', 'Anually')], default='monthly', max_length=13),
        ),
        migrations.AlterField(
            model_name='property',
            name='status',
            field=models.CharField(choices=[('rented', 'Rented'), ('available', 'Available'), ('under service', 'Under Service'), ('unavailable', 'Unavailable'), ('sold out', 'Sold Out')], default='available', max_length=15),
        ),
        migrations.AlterField(
            model_name='rental',
            name='lease_end_date',
            field=models.DateField(default=datetime.datetime(2024, 4, 19, 20, 47, 29, 167958, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='rental',
            name='lease_start_date',
            field=models.DateField(default=datetime.datetime(2024, 3, 20, 20, 47, 29, 166960, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='rental',
            name='rent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
