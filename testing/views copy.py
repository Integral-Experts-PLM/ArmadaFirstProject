import pprint
import json
from django.http import JsonResponse
from django.conf import settings
import requests
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import IncidentInfo, EquipmentDetails, LocationDetails, MaintenanceInfo, IncidentDetail, IncidentAnalysis
from .forms import IncidentInfoForm, EquipmentDetailsForm, LocationDetailsForm, MaintenanceInfoForm, IncidentDetailForm, IncidentAnalysisForm, IncidentInfoIdForm


def home(request):
    message = None  # Initialize the message variable
    incident_ID_form = IncidentInfoIdForm(request.POST or None)

    if request.method == 'POST':
        if incident_ID_form.is_valid():
            incident_ID = incident_ID_form.cleaned_data['incident_ID']
            system_id = incident_ID_form.cleaned_data['system_id']
            project_id = incident_ID_form.cleaned_data['project_id']

            url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}'

            auth = (settings.API_USERNAME, settings.API_PASSWORD)

            response = requests.get(url, auth=auth)
            if response.status_code == 200:
                return redirect('view_incident', project_id=project_id, system_id=system_id, incident_ID=incident_ID)
            else:
                message = 'Invalid Incident Credentials!'
        else:
            message = 'All Fields Are Required!'
    else:
        incident_ID_form = IncidentInfoIdForm()

    context = {'incident_ID_form': incident_ID_form, 'message': message}
    return render(request, 'base/home.html', context)


def createIncident(request):
    # Create forms for the incident creation
    incident_info_form = IncidentInfoForm(request.POST or None)
    equipment_details_form = EquipmentDetailsForm(request.POST or None)
    location_details_form = LocationDetailsForm(request.POST or None)
    incident_details_form = IncidentDetailForm(request.POST or None)

    if request.method == 'POST':
        if all([incident_info_form.is_valid(), equipment_details_form.is_valid(), location_details_form.is_valid(), incident_details_form.is_valid()]):

            incident_data = incident_info_form.save(commit=False)
            incident_data.save()

            equipment_data = equipment_details_form.save(commit=False)
            equipment_data.incident_ID = incident_data
            equipment_data.save()

            location_details = location_details_form.save(commit=False)
            location_details.incident_ID = incident_data
            location_details.save()

            incident_details = incident_details_form.save(commit=False)
            incident_details.incident_ID = incident_data
            incident_details.save()

            return redirect('home')
        else:
            incident_info_form = IncidentInfoForm()
            equipment_details_form = EquipmentDetailsForm()
            location_details_form = LocationDetailsForm()
            incident_details_form = IncidentDetailForm()

    context = {'incident_info_form': incident_info_form, 'equipment_details_form': equipment_details_form, 'location_details_form': location_details_form, 'incident_details_form': incident_details_form, 'view': 'create_incident'
               }

    return render(request, 'base/createIncident.html', context)


def incidentReviewAnalysis(request):
    # UNDER CONSTRUCTION
    # incident = get_object_or_404(IncidentInfo.objects.select_related('initial_info', 'detail_info', 'review', 'analysis'), pk=str(pk))
    # context = {'incident': incident}

    return render(request, 'base/incidentReviewAnalysis.html')


def updateIncident(request, pk):
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

            return redirect('view_incident', pk=incident.pk)
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


def deleteIncident(request, pk):
    # Use get_object_or_404 to retrieve the IncidentInfo instance
    incident = get_object_or_404(IncidentInfo, pk=pk)

    if request.method == 'POST':
        incident.delete()
        return redirect('home')

    context = {'incident': incident, 'view': 'delete_incident', }
    return render(request, 'base/deleteIncident.html', context)


def viewIncident(request, project_id, system_id, incident_ID):

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}'

    auth = (settings.API_USERNAME, settings.API_PASSWORD)

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()

        # Convert data to a JSON string with indentation for readability
        formatted_data = json.dumps(data, indent=4)

        # Create a HttpResponse with the formatted JSON data
        response = HttpResponse(formatted_data, content_type="application/json")

        return response
        # return redirect('view_incident', pk=incident.pk)
        
        context = {
        'incident': incident,
        'equipment_details': equipment_details,
        'location_details': location_details,
        'maintenance_info': maintenance_info,
        'incident_details': incident_details,
        'incident_analysis': incident_analysis,
        'view': 'view_incident',
        }

    # Render the template and pass the context
    return render(request, 'base/viewIncident.html', context)

    else:
        message = 'Invalid Incident Credentials!'
        incident_ID_form = IncidentInfoIdForm()


    # # Use get_object_or_404 to retrieve the IncidentInfo instance
    # incident = get_object_or_404(IncidentInfo, pk=pk)

    # # Access related objects with correct lowercase names
    # equipment_details = EquipmentDetails.objects.filter(
    #     incident_ID=incident).first()
    # location_details = LocationDetails.objects.filter(
    #     incident_ID=incident).first()
    # maintenance_info = MaintenanceInfo.objects.filter(
    #     incident_ID=incident).first()
    # incident_details = IncidentDetail.objects.filter(
    #     incident_ID=incident).first()
    # incident_analysis = IncidentAnalysis.objects.filter(
    #     incident_ID=incident).first()

    # context = {
    #     'incident': incident,
    #     'equipment_details': equipment_details,
    #     'location_details': location_details,
    #     'maintenance_info': maintenance_info,
    #     'incident_details': incident_details,
    #     'incident_analysis': incident_analysis,
    #     'view': 'view_incident',
    # }

    # # Render the template and pass the context
    # return render(request, 'base/viewIncident.html', context)


def insert_new_record(request):
    # Add your logic here to insert a new record for the  MAINTENANCE
    # UNDER CONSTRUCTION
    # For example, you can save data to the database or perform any desired action.
    # You can customize the response as needed.
    return HttpResponse("New record inserted successfully")


    #     # Create a pretty printer
    #     pretty_printer = pprint.PrettyPrinter(indent=4)

    #     # Print the incident data
    #     print("IncidentInfo Data:")
    #     pretty_printer.pprint(incident.__dict__)
