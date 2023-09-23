from django.forms import ModelForm
from .models import IncidentInfo, EquipmentDetails, LocationDetails, MaintananceInfo, IncidentDetail, IncidentAnalysis

class IncidentInfoForm(ModelForm):
    class Meta:
        model = IncidentInfo
        exclude = ['current_state']

class EquipmentDetailsForm(ModelForm):
    class Meta:
        model = EquipmentDetails
        exclude = ['incident_id']

class LocationDetailsForm(ModelForm):
    class Meta:
        model = LocationDetails
        fields = '__all__'

class MaintananceInfoForm(ModelForm):
    class Meta:
        model = MaintananceInfo
        fields = '__all__'

class IncidentDetailForm(ModelForm):
    class Meta:
        model = IncidentDetail
        fields = '__all__'

class IncidentAnalysisForm(ModelForm):
    class Meta:
        model = IncidentAnalysis
        fields = '__all__'
