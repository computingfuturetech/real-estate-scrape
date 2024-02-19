# Generated by Django 5.0.1 on 2024-02-19 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_apartmentdetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField(unique=True)),
                ('project_name', models.CharField(max_length=500)),
                ('last_inspected', models.DateField()),
                ('completion', models.CharField(max_length=50)),
                ('handover', models.DateField()),
            ],
        ),
    ]