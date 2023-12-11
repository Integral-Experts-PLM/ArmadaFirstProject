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
    meter_reading_tsn = models.FloatField(null=True, blank=True)
    time_to_failure_tso = models.FloatField(null=True, blank=True)
    user_text10_oem = models.CharField(max_length=200, null=True, blank=True)
    analysis_team = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.incident_ID.incident_ID)

class LocationDetails(models.Model):
    incident_ID = models.ForeignKey(IncidentInfo, on_delete=models.CASCADE)
    user_text4_location = models.CharField(max_length=200, null=True, blank=True)
    user_text24_address = models.TextField(null=True, blank=True)
    user_text24_city = models.CharField(max_length=200, null=True, blank=True)
    user_text16_zip = models.CharField(max_length=200, null=True, blank=True)
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
    attachments_incidents = models.CharField(max_length=200, null=True, blank=True)

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

class OperatingTimes(models.Model):
    identifier = models.CharField(max_length=200, null=True, blank=True)
    configuration = models.CharField(max_length=200, null=True, blank=True)
    user_text1_tail_number = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    operational_time = models.FloatField(null=True, blank=True)
    multiplicative_djustment = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.identifier)

class CreateIncident(models.Model):
    identifier = models.CharField(max_length=200, null=True, blank=True)
    project_id = models.CharField(max_length=200)
    system_id = models.CharField(max_length=200)
    configuration = models.CharField(max_length=200,)
    system_tree_item = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    user_text22_failure_detection_situation = models.CharField(max_length=200, null=True, blank=True)
    user_text23_failure_buque_situation = models.CharField(max_length=200, null=True, blank=True)
    user_text24_failure_effect_item = models.CharField(max_length=200, null=True, blank=True)
    user_text25_failure_evidence = models.CharField(max_length=200, null=True, blank=True)
    occurrence_date = models.DateTimeField()
    # occurrence_time = models.CharField(max_length=200, null=True, blank=True)
    description_incident =  models.TextField(null=True, blank=True)
    user_text26_user_failure_detection = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.identifier
    


class Incident(models.Model):
    ID = models.AutoField(primary_key=True)  # ID (PK, int, not null)
    Identifier = models.CharField(max_length=255, blank=True, null=True)  # Identifier (nvarchar(255), null)
    DateStart = models.DateTimeField(null=True)
    SetID = models.IntegerField(null=True)
    IncUserText26 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText27 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText28 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText29 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText30 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText31 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText32 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText33 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText34 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText35 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText36 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText37 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText38 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText39 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText40 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText41 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText42 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText43 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText44 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText45 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText46 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText47 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText48 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText49 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText50 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText51 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText52 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText53 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText54 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText55 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText56 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText57 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText58 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText59 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText60 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText61 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText62 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText63 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText64 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText65 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText66 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText67 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText68 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText69 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText70 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText71 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText72 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText73 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText74 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText75 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText76 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText77 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText78 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText79 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText80 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText81 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText82 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText83 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText84 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText85 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText86 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText87 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText88 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText89 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText90 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText91 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText92 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText93 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText94 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText95 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText96 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText97 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText98 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText99 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText100 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText101 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText102 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText103 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText104 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText105 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText106 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText107 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText108 = models.CharField(max_length=255, blank=True, null=True)
    IncUserText109 = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        managed = False  # Indica que Django no debe gestionar la creación de la tabla
        db_table = 'Incidents1'