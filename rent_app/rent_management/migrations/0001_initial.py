# Generated by Django 5.0.3 on 2024-03-22 01:05

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('line1', models.CharField(max_length=50)),
                ('line2', models.CharField(blank=True, max_length=50, null=True)),
                ('zipcode', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='ReferencePerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=10)),
                ('last_name', models.CharField(blank=True, max_length=10, null=True)),
                ('phone_num', models.CharField(blank=True, max_length=12, null=True)),
                ('email', models.EmailField(blank=True, max_length=80, null=True)),
                ('relationship', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('flat', 'Flat'), ('house', 'House'), ('condo', 'Condo'), ('shop', 'Shop'), ('townhouse', 'Townhouse'), ('bungalow', 'Bungalow'), ('other', 'Other')], max_length=15)),
                ('other_type', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(choices=[('rented', 'Rented'), ('available', 'Available'), ('under service', 'Under Service'), ('unavailable', 'Unavailable'), ('sold out', 'Sold Out')], default='available', max_length=15)),
                ('payment_freq', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annually', 'Anually')], default='monthly', max_length=9)),
                ('default_rent', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rent_management.address')),
            ],
            options={
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=10)),
                ('last_last', models.CharField(max_length=10)),
                ('phone_num', models.CharField(blank=True, max_length=12, null=True)),
                ('email', models.CharField(blank=True, max_length=80, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rent_management.address')),
                ('reference', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rent_management.referenceperson')),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lease_start_date', models.DateField(default=datetime.datetime(2024, 3, 22, 1, 5, 28, 483566, tzinfo=datetime.timezone.utc))),
                ('lease_end_date', models.DateField(default=datetime.datetime(2024, 4, 21, 1, 5, 28, 483566, tzinfo=datetime.timezone.utc))),
                ('lease_duration', models.DurationField(blank=True, default=datetime.timedelta(days=30), null=True)),
                ('rent', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('rental_freq', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annually', 'Anually')], default='monthly', max_length=13)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rent_management.property')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rent_management.tenant')),
            ],
        ),
    ]
