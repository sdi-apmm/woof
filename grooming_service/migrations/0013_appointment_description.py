# Generated by Django 5.0.4 on 2024-05-12 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grooming_service', '0012_remove_appointment_end_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
