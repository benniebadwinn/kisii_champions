# Generated by Django 5.0.1 on 2024-01-18 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holiday_off', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='remaining_days',
            field=models.IntegerField(default=0),
        ),
    ]
