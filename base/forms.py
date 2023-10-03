from django.forms import ModelForm, forms
from .models import IncidentInfo, EquipmentDetails, LocationDetails, MaintananceInfo, IncidentDetail, IncidentAnalysis

class IncidentInfoIdForm(ModelForm):
    class Meta:
        model = IncidentInfo
        fields = ['incident_id', 'system_id', 'project_id']

class IncidentCreationForm(ModelForm):
    class Meta:
        model = IncidentInfo
        fields = ['system_id', 'project_id']

# 'current_state' must be exclude because it has a default initial value
class IncidentInfoForm(ModelForm):
    class Meta:
        model = IncidentInfo
        exclude = ['current_state', 'project_id', 'system_id', 'incident_id']

# 'incident_id' must be exclude because it is asign automaticaly
class EquipmentDetailsForm(ModelForm):
    class Meta:
        model = EquipmentDetails
        exclude = ['incident_id']

# 'incident_id' must be exclude because it is asign automaticaly
class LocationDetailsForm(ModelForm):
    class Meta:
        model = LocationDetails
        exclude = ['incident_id']

class MaintananceInfoForm(ModelForm):
    class Meta:
        model = MaintananceInfo
        exclude = ['incident_id']

# 'incident_id' must be exclude because it is asign automaticaly
class IncidentDetailForm(ModelForm):
    class Meta:
        model = IncidentDetail
        exclude = ['incident_id']

class IncidentAnalysisForm(ModelForm):
    class Meta:
        model = IncidentAnalysis
        fields = '__all__'
