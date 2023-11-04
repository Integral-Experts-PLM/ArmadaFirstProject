from django.forms import ModelForm, forms
from .models import IncidentInfo, EquipmentDetails, LocationDetails, MaintenanceInfo, IncidentDetail, IncidentAnalysis, OperatingTimes

class IncidentInfoIdForm(ModelForm):
    class Meta:
        model = IncidentInfo
        fields = ['incident_ID', 'system_id', 'project_id']

class IncidentCreationForm(ModelForm):
    class Meta:
        model = IncidentInfo
        fields = ['system_id', 'project_id']

# 'workflow_state' must be exclude because it has a default initial value
class IncidentInfoForm(ModelForm):
    class Meta:
        model = IncidentInfo
        exclude = ['workflow_state', 'project_id', 'system_id', 'incident_ID']

# 'incident_ID' must be exclude because it is asign automaticaly
class EquipmentDetailsForm(ModelForm):
    class Meta:
        model = EquipmentDetails
        exclude = ['incident_ID']

# 'incident_ID' must be exclude because it is asign automaticaly
class LocationDetailsForm(ModelForm):
    class Meta:
        model = LocationDetails
        exclude = ['incident_ID']

class MaintenanceInfoForm(ModelForm):
    class Meta:
        model = MaintenanceInfo
        exclude = ['incident_ID', 'maintenance_log_identifier']

# 'incident_ID' must be exclude because it is asign automaticaly
class IncidentDetailForm(ModelForm):
    class Meta:
        model = IncidentDetail
        exclude = ['incident_ID']

class IncidentAnalysisForm(ModelForm):
    class Meta:
        model = IncidentAnalysis
        fields = '__all__'

# 'operational_time' must be exclude because it not editable
# this is an console error, ask armada
class operatingTimesForm(ModelForm):
    class Meta:
        model = OperatingTimes
        exclude = ['operational_time']