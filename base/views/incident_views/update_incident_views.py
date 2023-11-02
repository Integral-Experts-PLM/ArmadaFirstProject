import requests
import json
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from ...models import IncidentInfo, EquipmentDetails, LocationDetails, MaintenanceInfo, IncidentDetail, IncidentAnalysis
from ...forms import IncidentInfoForm, EquipmentDetailsForm, LocationDetailsForm, MaintenanceInfoForm, IncidentDetailForm, IncidentAnalysisForm, IncidentInfoIdForm, IncidentCreationForm
from datetime import datetime

def updateIncident(request):
    # Use get_object_or_404 to retrieve the IncidentInfo instance
    incident = get_object_or_404(IncidentInfo, pk=pk)

    # Access related objects
    equipment_details = EquipmentDetails.objects.filter(
        incident_ID=incident).first()
    location_details = LocationDetails.objects.filter(
        incident_ID=incident).first()
    incident_details = IncidentDetail.objects.filter(
        incident_ID=incident).first()

    if request.method == 'POST':
        # Create forms instances to be updated
        incident_info_form = IncidentInfoForm(request.POST, instance=incident)
        equipment_details_form = EquipmentDetailsForm(
            request.POST, instance=equipment_details)
        location_details_form = LocationDetailsForm(
            request.POST, instance=location_details)
        incident_details_form = IncidentDetailForm(
            request.POST, instance=incident_details)

        if all([incident_info_form.is_valid(), equipment_details_form.is_valid(), location_details_form.is_valid(), incident_details_form.is_valid()]):
            # Save the updated data
            incident_info_form.save()
            equipment_details_form.save()
            location_details_form.save()
            incident_details_form.save()

            return redirect('view_all_incidents', pk=incident.pk)
    else:
        # Initialize forms with existing data
        incident_info_form = IncidentInfoForm(instance=incident)
        equipment_details_form = EquipmentDetailsForm(
            instance=equipment_details)
        location_details_form = LocationDetailsForm(instance=location_details)
        incident_details_form = IncidentDetailForm(instance=incident_details)

    context = {
        'incident': incident,
        'equipment_details': equipment_details,
        'location_details': location_details,
        'incident_details': incident_details,
        'view': 'update_incident',
    }
    return render(request, 'base/updateIncident.html', context)