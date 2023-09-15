from django.forms import ModelForm
from .models import Incident

class IncidentForm(ModelForm):
    class Meta:
        model = Incident
        fields = '__all__'
