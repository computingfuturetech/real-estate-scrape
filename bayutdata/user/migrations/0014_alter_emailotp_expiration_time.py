# Generated by Django 5.0.1 on 2024-02-16 09:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_emailotp_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailotp',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 16, 9, 58, 59, 514869, tzinfo=datetime.timezone.utc)),
        ),
    ]
