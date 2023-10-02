from django.db import models
from django.contrib.auth.models import User

class IncidentInfo(models.Model):
    incident_id = models.CharField(max_length=200)
    system_id = models.CharField(max_length=200)
    project_id = models.CharField(max_length=200)
    current_state = models.CharField(max_length=200, default='NEW INCIDENT')
    reportedBy = models.CharField(max_length=200, null=True, blank=True)
    incident_date = models.DateTimeField()
    configuration = models.CharField(max_length=200, null=True, blank=True)
    tail_number = models.CharField(max_length=200, null=True, blank=True)
    mission_effect = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.incident_id

class EquipmentDetails(models.Model):
    incident_id = models.ForeignKey(IncidentInfo, on_delete=models.CASCADE)
    failed_component = models.CharField(max_length=200, null=True, blank=True)
    serial_number = models.CharField(max_length=200, null=True, blank=True)
    tsn = models.CharField(max_length=200, null=True, blank=True)
    tso = models.CharField(max_length=200, null=True, blank=True)
    oem = models.CharField(max_length=200, null=True, blank=True)
    analysis_team = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.incident_id.incident_id)

class LocationDetails(models.Model):
    incident_id = models.ForeignKey(IncidentInfo, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.incident_id.incident_id)

class MaintananceInfo(models.Model):
    incident_id = models.ForeignKey(IncidentInfo, on_delete=models.CASCADE)
    field_1 = models.CharField(max_length=200, null=True, blank=True)
    field_2 = models.CharField(max_length=200, null=True, blank=True)
    field_3 = models.CharField(max_length=200, null=True, blank=True)
    field_4 = models.CharField(max_length=200, null=True, blank=True)
    field_5 = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.incident_id.incident_id)

class IncidentDetail(models.Model):
    incident_id = models.ForeignKey(IncidentInfo, on_delete=models.CASCADE)
    operating_mode = models.CharField(max_length=200, null=True, blank=True)
    initial_severity = models.CharField(max_length=200, null=True, blank=True)
    incident_description = models.TextField(null=True, blank=True)
    maintenance = models.ForeignKey(MaintananceInfo, on_delete=models.CASCADE, null=True, blank=True)
    attachment = models.FileField(null=True, blank=True)

    def __str__(self):
        return str(self.incident_id.incident_id)

class IncidentAnalysis(models.Model):
    incident_id = models.ForeignKey(IncidentInfo, on_delete=models.CASCADE)
    team_analysis = models.CharField(max_length=200, null=True, blank=True)
    failure_detection = models.CharField(max_length=200, null=True, blank=True)
    failure_mode = models.CharField(max_length=200, null=True, blank=True)
    part_category = models.CharField(max_length=200, null=True, blank=True)
    root_cause = models.CharField(max_length=200, null=True, blank=True)
    analysis_result = models.TextField(null=True, blank=True)
    analysis_recomendation = models.TextField(null=True, blank=True)
    attachment = models.FileField(null=True, blank=True)

    def __str__(self):
        return str(self.incident_id.incident_id)
    