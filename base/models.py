from django.db import models
from django.contrib.auth.models import User

class IncidentInfo(models.Model):
    incident_ID = models.CharField(max_length=200, unique=True)
    system_id = models.CharField(max_length=200)
    project_id = models.CharField(max_length=200)
    workflow_state = models.CharField(max_length=200, default='NEW INCIDENT')
    person_incident_entry = models.CharField(max_length=200, null=True, blank=True)
    occurrence_date = models.DateTimeField()
    configuration = models.CharField(max_length=200, null=True, blank=True)
    user_text13_tail_number = models.CharField(max_length=200, null=True, blank=True)
    user_text17_mission_effect = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.incident_ID

class EquipmentDetails(models.Model):
    incident_ID = models.ForeignKey(IncidentInfo, on_delete=models.CASCADE)
    failed_component = models.CharField(max_length=200, null=True, blank=True)
    serial_number = models.CharField(max_length=200, null=True, blank=True)
    meter_reading_tsn = models.CharField(max_length=200, null=True, blank=True)
    time_to_failure_tso = models.CharField(max_length=200, null=True, blank=True)
    user_text10_oem = models.CharField(max_length=200, null=True, blank=True)
    analysis_team = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.incident_ID.incident_ID)

class LocationDetails(models.Model):
    incident_ID = models.ForeignKey(IncidentInfo, on_delete=models.CASCADE)
    user_text4_location = models.CharField(max_length=200, null=True, blank=True)
    user_text24_address = models.TextField(null=True, blank=True)
    user_text25_contact = models.CharField(max_length=200, null=True, blank=True)
    user_text22_phone = models.CharField(max_length=200, null=True, blank=True)
    user_text21_email = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.incident_ID.incident_ID)

class MaintenanceInfo(models.Model):
    incident_ID = models.ForeignKey(IncidentInfo, on_delete=models.CASCADE)
    maintenance_log_identifier = models.CharField(max_length=200)
    override_system_tree_item_replaced_part = models.CharField(max_length=200, null=True, blank=True)
    cost_item = models.FloatField(null=True, blank=True)
    elapsed_maintenance_time = models.FloatField(null=True, blank=True)
    cost_maintenance = models.FloatField(null=True, blank=True)
    number_of_men = models.IntegerField(null=True, blank=True)
    maintenance_start_date = models.DateTimeField()
    total_maintenance_time = models.FloatField(null=True, blank=True)
    user_value2_total_maintenance_time = models.FloatField(null=True, blank=True)
    action_taken_maintenace = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.incident_ID.incident_ID)

class IncidentDetail(models.Model):
    incident_ID = models.ForeignKey(IncidentInfo, on_delete=models.CASCADE)
    operating_mode = models.CharField(max_length=200, null=True, blank=True)
    user_text2_initial_severity = models.CharField(max_length=200, null=True, blank=True)
    description_incident = models.TextField(null=True, blank=True)
    maintenance = models.ForeignKey(MaintenanceInfo, on_delete=models.CASCADE, null=True, blank=True)
    attachments_incidents = models.FileField(null=True, blank=True)

    def __str__(self):
        return str(self.incident_ID.incident_ID)

class IncidentAnalysis(models.Model):
    incident_ID = models.ForeignKey(IncidentInfo, on_delete=models.CASCADE)
    user_text11_team_analysis = models.CharField(max_length=200, null=True, blank=True)
    failure_detection = models.CharField(max_length=200, null=True, blank=True)
    failure_mode = models.CharField(max_length=200, null=True, blank=True)
    user_text16_part_category = models.CharField(max_length=200, null=True, blank=True)
    root_cause = models.CharField(max_length=200, null=True, blank=True)
    analysis_result = models.TextField(null=True, blank=True)
    analysis_recomendation = models.TextField(null=True, blank=True)
    attachments_analysis = models.FileField(null=True, blank=True)

    def __str__(self):
        return str(self.incident_ID.incident_ID)
    