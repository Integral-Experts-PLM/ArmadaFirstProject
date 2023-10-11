from django.contrib import admin

# Register your models here.
from .models import IncidentInfo
from .models import EquipmentDetails
from .models import LocationDetails
from .models import MaintenanceInfo
from .models import IncidentDetail
from .models import IncidentAnalysis

admin.site.register(IncidentInfo)
admin.site.register(EquipmentDetails)
admin.site.register(LocationDetails)
admin.site.register(MaintenanceInfo)
admin.site.register(IncidentDetail)
admin.site.register(IncidentAnalysis)