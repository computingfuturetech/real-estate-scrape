# Generated by Django 5.0.1 on 2024-02-19 07:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_alter_emailotp_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailotp',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 19, 7, 9, 38, 367211, tzinfo=datetime.timezone.utc)),
        ),
    ]