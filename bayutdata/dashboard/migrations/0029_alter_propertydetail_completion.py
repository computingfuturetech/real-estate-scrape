# Generated by Django 5.0.1 on 2024-02-29 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0028_propertydetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertydetail',
            name='completion',
            field=models.CharField(default='Ready', max_length=50),
        ),
    ]
