# Generated by Django 5.0.1 on 2024-02-28 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0023_projectinformation_apartment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectinformation',
            name='apartment_id',
        ),
        migrations.AddField(
            model_name='apartmentdetail',
            name='title',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
