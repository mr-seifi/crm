# Generated by Django 4.1.2 on 2022-10-20 16:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_alter_customer_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliance',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appliance',
            name='price',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
