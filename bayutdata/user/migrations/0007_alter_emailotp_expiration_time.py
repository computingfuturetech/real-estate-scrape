# Generated by Django 5.0.1 on 2024-02-15 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_emailotp_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailotp',
            name='expiration_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]