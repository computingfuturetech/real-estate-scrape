# Generated by Django 5.0.1 on 2024-02-28 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_remove_projectinformation_apartment_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertydetail',
            name='state',
            field=models.CharField(default='Dubai', max_length=100),
        ),
        migrations.AddField(
            model_name='propertydetail',
            name='sub_state',
            field=models.CharField(default='Dubai Marina', max_length=100),
        ),
    ]