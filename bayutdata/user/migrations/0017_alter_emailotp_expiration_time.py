# Generated by Django 5.0.1 on 2024-02-16 12:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_alter_emailotp_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailotp',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 16, 12, 22, 6, 765368, tzinfo=datetime.timezone.utc)),
        ),
    ]
