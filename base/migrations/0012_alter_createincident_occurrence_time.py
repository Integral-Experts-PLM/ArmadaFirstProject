# Generated by Django 4.2.5 on 2023-11-07 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_createincident'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createincident',
            name='occurrence_time',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
