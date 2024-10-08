# Generated by Django 5.1 on 2024-08-15 07:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermngt', '0006_application_mobile_application_photo_employee_mobile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='mobile',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(message='enter the number in xxx-xxx-xxxx formate', regex='^[d{10}]$')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='mobile',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(message='enter the number in xxx-xxx-xxxx formate', regex='^[d{10}]$')]),
        ),
    ]
