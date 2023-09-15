# Generated by Django 4.2.5 on 2023-09-13 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IncidentAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_identifier', models.CharField(max_length=200)),
                ('method', models.FileField(blank=True, null=True, upload_to='')),
                ('investigation_done', models.TextField(blank=True, null=True)),
                ('analysis_results', models.TextField(blank=True, null=True)),
                ('failure_mode', models.CharField(max_length=200)),
                ('root_cause', models.CharField(max_length=200)),
                ('date_analysed', models.DateTimeField()),
                ('incident_attachment', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='IncidentDetailInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_identifier', models.CharField(max_length=200)),
                ('failure_mode', models.CharField(blank=True, max_length=200, null=True)),
                ('failure_symptom', models.CharField(blank=True, max_length=200, null=True)),
                ('incident_description', models.TextField(blank=True, null=True)),
                ('incident_date', models.DateTimeField()),
                ('notice_date', models.DateTimeField()),
                ('relevant_category', models.CharField(max_length=200)),
                ('remark_incident_entry', models.TextField(blank=True, null=True)),
                ('incident_attachment', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='IncidentInitialInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_identifier', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('configuration', models.CharField(max_length=200)),
                ('related_part', models.CharField(max_length=200)),
                ('user', models.CharField(max_length=200)),
                ('incident_date', models.DateTimeField()),
                ('serial_number', models.CharField(max_length=200)),
                ('initial_records', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IncidentReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_identifier', models.CharField(max_length=200)),
                ('incident_type', models.CharField(max_length=200)),
                ('incident_fracas_description', models.TextField(blank=True, null=True)),
                ('part_name', models.CharField(max_length=200)),
                ('part_number', models.CharField(max_length=200)),
                ('serial_number', models.CharField(max_length=200)),
                ('project_number', models.CharField(max_length=200)),
                ('project_name', models.CharField(max_length=200)),
                ('customer_number', models.CharField(max_length=200)),
                ('customer_name', models.CharField(max_length=200)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(max_length=200)),
                ('operating_mode', models.CharField(max_length=200)),
                ('corrective_maintenance', models.CharField(max_length=200)),
                ('incident_attachment', models.FileField(blank=True, null=True, upload_to='')),
                ('recommendation', models.TextField(blank=True, null=True)),
                ('analysis_team', models.CharField(max_length=200)),
                ('rca_needed', models.CharField(max_length=200)),
                ('bd_needed', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_state', models.CharField(default='NEW INCIDENT', max_length=200)),
                ('incident_identifier', models.CharField(max_length=200)),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.incidentanalysis')),
                ('detail_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.incidentdetailinfo')),
                ('initial_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.incidentinitialinfo')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.incidentreview')),
            ],
        ),
    ]