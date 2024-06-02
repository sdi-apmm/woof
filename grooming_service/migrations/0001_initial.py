# Generated by Django 5.0.4 on 2024-04-30 22:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
            options={
                'db_table': 'woof_wash_grooming"."Service',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField()),
                ('phone_number', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'woof_wash_grooming"."User',
            },
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_name', models.CharField(max_length=255)),
                ('breed', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('medical_notes', models.TextField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grooming_service.user')),
            ],
            options={
                'db_table': 'woof_wash_grooming"."Pet',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField()),
                ('start_date_time', models.DateTimeField()),
                ('end_date_time', models.DateTimeField()),
                ('pet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grooming_service.pet')),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grooming_service.service')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grooming_service.user')),
            ],
            options={
                'db_table': 'woof_wash_grooming"."Appointment',
            },
        ),
    ]