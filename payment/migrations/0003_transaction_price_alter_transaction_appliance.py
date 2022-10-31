# Generated by Django 4.1.2 on 2022-10-20 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_alter_appliance_description_alter_appliance_price'),
        ('payment', '0002_alter_transaction_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='appliance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.appliance'),
        ),
    ]
