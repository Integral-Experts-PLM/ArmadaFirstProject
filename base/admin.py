from django.contrib import admin

# Register your models here.
from .models import IncidentInitialInfo
from .models import IncidentDetailInfo
from .models import IncidentReview
from .models import IncidentAnalysis
from .models import Incident

admin.site.register(IncidentInitialInfo)
admin.site.register(IncidentDetailInfo)
admin.site.register(IncidentReview)
admin.site.register(IncidentAnalysis)
admin.site.register(Incident)