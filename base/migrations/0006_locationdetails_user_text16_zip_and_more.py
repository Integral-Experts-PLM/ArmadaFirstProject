# Generated by Django 4.2.5 on 2023-10-17 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_equipmentdetails_meter_reading_tsn_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationdetails',
            name='user_text16_zip',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='locationdetails',
            name='user_text24_city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
