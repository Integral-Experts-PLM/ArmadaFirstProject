from django.db import models

class TreeItem(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False  # Indica que Django no debe gestionar la creación, modificación ni eliminación de la tabla correspondiente en la base de datos
        db_table = 'System'


class Incident(models.Model):
    ID = models.AutoField(primary_key=True)  # ID (PK, int, not null)
    Identifier = models.CharField(max_length=255, blank=True, null=True)  # Identifier (nvarchar(255), null)
    DateIncident = models.DateTimeField(null=True)
    DateEndCO = models.DateTimeField(null=True)
    IncidentDescription = models.CharField(max_length=255, blank=True, null=True)
    SetID = models.IntegerField(null=True)
    ConfigurationID = models.IntegerField(null=True)
    TreeID = models.ForeignKey(TreeItem, on_delete=models.SET_NULL, null=True, blank=True, db_column='TreeID')
    IncidentUser = models.CharField(max_length=255, blank=True, null=True)
    IncUserText2 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False  # Indica que Django no debe gestionar la creación, modificación ni eliminación de la tabla correspondiente en la base de datos
        db_table = 'Incidents1'




# class MaintenanceLog(models.Model):
#     IncidentID = models.IntegerField(null=True)
#     Identifier = models.CharField(max_length=255, blank=True, null=True)
#     DateStart = models.DateTimeField(null=True)
#     SetID = models.IntegerField(null=True)
#     ConfigurationID = models.IntegerField(null=True)
#     TreeID = models.IntegerField(null=True)

#     class Meta:
#         managed = False  # Indica que Django no debe gestionar la creación de la tabla
#         db_table = 'Incidents1'