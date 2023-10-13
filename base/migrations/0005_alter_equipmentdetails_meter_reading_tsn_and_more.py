# Generated by Django 4.2.5 on 2023-10-13 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_incidentinfo_incident_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentdetails',
            name='meter_reading_tsn',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipmentdetails',
            name='time_to_failure_tso',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incidentdetail',
            name='attachments_incidents',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
