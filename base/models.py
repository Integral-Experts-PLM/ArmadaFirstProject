from django.db import models

class IncidentInitialInfo(models.Model):
    incident_identifier = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    configuration = models.CharField(max_length=200, null=True, blank=True)
    related_part = models.CharField(max_length=200, null=True, blank=True)
    user = models.CharField(max_length=200)
    incident_type = models.CharField(max_length=200)
    incident_date = models.DateTimeField()
    serial_number = models.CharField(max_length=200, null=True, blank=True)
    initial_records = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.incident_identifier

class IncidentDetailInfo(models.Model):
    incident_identifier = models.CharField(max_length=200)
    failure_mode = models.CharField(max_length=200, null=True, blank=True)
    failure_symptom = models.CharField(max_length=200, null=True, blank=True)
    fracas_incident_description = models.TextField(null=True, blank=True)
    incident_date = models.DateTimeField()
    notice_date = models.DateTimeField()
    relevant_category = models.CharField(max_length=200, null=True, blank=True)
    remark_incident_entry = models.TextField(null=True, blank=True)
    incident_attachment = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.incident_identifier
    
class IncidentReview(models.Model):
    incident_identifier = models.CharField(max_length=200)
    incident_description = models.TextField(null=True, blank=True)
    part_name = models.CharField(max_length=200, null=True, blank=True)
    part_number = models.CharField(max_length=200, null=True, blank=True)
    serial_number = models.CharField(max_length=200, null=True, blank=True)
    project_number = models.CharField(max_length=200, null=True, blank=True)
    project_name = models.CharField(max_length=200, null=True, blank=True)
    customer_number = models.CharField(max_length=200, null=True, blank=True)
    customer_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    operating_mode = models.CharField(max_length=200, null=True, blank=True)
    corrective_maintenance = models.CharField(max_length=200, null=True, blank=True)
    recommendation = models.TextField(null=True, blank=True)
    analysis_team = models.CharField(max_length=200, null=True, blank=True)
    rca_needed = models.CharField(max_length=200, null=True, blank=True)
    bd_needed = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.incident_identifier

class IncidentAnalysis(models.Model):
    incident_identifier = models.CharField(max_length=200)
    method = models.FileField(null=True, blank=True)
    investigation_done = models.TextField(null=True, blank=True)
    analysis_results = models.TextField(null=True, blank=True)
    failure_mode = models.CharField(max_length=200, null=True, blank=True)
    root_cause = models.CharField(max_length=200, null=True, blank=True)
    date_analysed = models.DateTimeField()
    incident_attachment = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.incident_identifier

class Incident(models.Model):
    current_state = models.CharField(max_length=200, default='NEW INCIDENT')
    incident_identifier = models.CharField(max_length=200)
    initial_info = models.ForeignKey(IncidentInitialInfo, on_delete=models.CASCADE, null=True)
    detail_info = models.ForeignKey(IncidentDetailInfo, on_delete=models.CASCADE, null=True)
    review = models.ForeignKey(IncidentReview, on_delete=models.CASCADE, null=True)
    analysis = models.ForeignKey(IncidentAnalysis, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.incident_identifier

