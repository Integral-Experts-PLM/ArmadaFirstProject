import pprint
import json
from django.http import JsonResponse
from django.conf import settings
import requests
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import IncidentInfo, EquipmentDetails, LocationDetails, MaintananceInfo, IncidentDetail, IncidentAnalysis
from .forms import IncidentInfoForm, EquipmentDetailsForm, LocationDetailsForm, MaintananceInfoForm, IncidentDetailForm, IncidentAnalysisForm, IncidentInfoIdForm, IncidentCreationForm
from datetime import datetime

def home(request):
    message = None  # Initialize the message variable
    incident_id_form = IncidentInfoIdForm(request.POST or None)

    if request.method == 'POST':
        if incident_id_form.is_valid():
            incident_id = incident_id_form.cleaned_data['incident_id']
            system_id = incident_id_form.cleaned_data['system_id']
            project_id = incident_id_form.cleaned_data['project_id']

            url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_id}'

            auth = (settings.API_USERNAME, settings.API_PASSWORD)

            response = requests.get(url, auth=auth)
            if response.status_code == 200:
                return redirect('view_incident', project_id=project_id, system_id=system_id, incident_id=incident_id)
            else:
                message = 'Invalid Incident Credentials!'
        else:
            message = 'All Fields Are Required!'
    else:
        incident_id_form = IncidentInfoIdForm()

    context = {'incident_id_form': incident_id_form, 'message': message}
    return render(request, 'base/home.html', context)


def homeCreateIncident(request):
    message = None  # Initialize the message variable
    incident_creation_form = IncidentCreationForm(request.POST or None)

    if request.method == 'POST':
        if incident_creation_form.is_valid():
            system_id = incident_creation_form.cleaned_data['system_id']
            project_id = incident_creation_form.cleaned_data['project_id']

            url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents'

            auth = (settings.API_USERNAME, settings.API_PASSWORD)

            response = requests.get(url, auth=auth)

            if response.status_code == 200:
                return redirect('create_incident', project_id=project_id, system_id=system_id)
            else:
                message = 'Invalid Credentials!'
        else:
            message = 'All Fields Are Required!'
    else:
        incident_creation_form = IncidentCreationForm()

    context = {'incident_creation_form': incident_creation_form, 'message': message}
    return render(request, 'base/homeCreate.html', context)


def createIncident(request, project_id, system_id):
    # Create forms for the incident creation
    incident_info_form = IncidentInfoForm(request.POST or None)
    equipment_details_form = EquipmentDetailsForm(request.POST or None)
    location_details_form = LocationDetailsForm(request.POST or None)
    incident_details_form = IncidentDetailForm(request.POST or None)

    # Define authentication credentials
    auth = (settings.API_USERNAME, settings.API_PASSWORD)

    # Define base URL
    base_url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/'

    # Define URLs for configurations and tree items
    url_configuration = f'{base_url}Configurations'
    url_tree_items = f'{base_url}TreeItems'

    # Function to handle the API request and response
    def make_api_request(url):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = requests.get(url, auth=auth)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None  # Handle errors as needed

    # Get configuration and tree item data
    configuration_data = make_api_request(url_configuration)
    tree_items_data = make_api_request(url_tree_items)

    if configuration_data is not None and tree_items_data is not None:
        configuration = configuration_data.get('value', [])[0].get('ID')
        tree_items = tree_items_data.get('value', [])[0].get('ID')

        if request.method == 'POST' and incident_info_form.is_valid() and equipment_details_form.is_valid() and location_details_form.is_valid() and incident_details_form.is_valid():

            incident_data = incident_info_form.save(commit=False)

            equipment_data = equipment_details_form.save(commit=False)

            location_details = location_details_form.save(commit=False)

            incident_details = incident_details_form.save(commit=False)

            # Define the URL for creating an incident
            url_post = f'{base_url}Incidents'

            # Define the payload for creating an incident
            payload = {
                "PersonIncidentEntry": incident_data.reportedBy,
                "UserText13": incident_data.tail_number,
                "OccurrenceDate": incident_data.incident_date.strftime("%Y-%m-%dT%H:%M:%S+02:00"),
                # "OccurrenceDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+02:00"),

                "SerialNumber": equipment_data.serial_number,

                "UserText4": location_details.location,
                "UserText23": location_details.address,
                "UserText25": location_details.contact,
                "UserText22": location_details.phone,
                "UserText21": location_details.email,

                "OperatingMode": incident_details.operating_mode,
                "UserText2": incident_details.initial_severity,
                "DescriptionIncident": incident_details.incident_description,

                "Configuration@odata.bind": f"Systems({system_id})/Configurations({configuration})",
                "SystemTreeItem@odata.bind": f"Systems({system_id})/TreeItems({tree_items})"
            }

            # Set the headers for the request
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            # Convert the payload dictionary to a JSON string
            payload_json = json.dumps(payload)

            # Make the POST request to create an incident
            response = requests.post(url_post, data=payload_json, headers=headers, auth=auth)

            # Check the response
            if response.status_code == 201:
                print(f"Incident created: Date: {response.json()}")
                return redirect('view_incident', project_id=project_id, system_id=system_id, incident_id=response.json().get('ID'))
            else:
                print(f"Failed to create incident. Status code: {response.status_code}")
                print(response.text)  # Print the response content for debugging
        else:
            print('incident form not ok')
            context = {
            'incident_info_form': incident_info_form,
            'equipment_details_form': equipment_details_form,
            'location_details_form': location_details_form,
            'incident_details_form': incident_details_form,
            'view': 'create_incident'
        }
    else:
        print("Failed to retrieve configuration and tree item data.")

    return render(request, 'base/createIncident.html', context)


def incidentReviewAnalysis(request):
    # UNDER CONSTRUCTION
    # incident = get_object_or_404(IncidentInfo.objects.select_related('initial_info', 'detail_info', 'review', 'analysis'), pk=str(pk))
    # context = {'incident': incident}

    return render(request, 'base/incidentReviewAnalysis.html')


def updateIncident(request):

    # Use get_object_or_404 to retrieve the IncidentInfo instance
    incident = get_object_or_404(IncidentInfo, pk=pk)

    # Access related objects
    equipment_details = EquipmentDetails.objects.filter(
        incident_id=incident).first()
    location_details = LocationDetails.objects.filter(
        incident_id=incident).first()
    incident_details = IncidentDetail.objects.filter(
        incident_id=incident).first()

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


def viewIncident(request, project_id, system_id, incident_id):

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_id}'

    auth = (settings.API_USERNAME, settings.API_PASSWORD)

    response = requests.get(url, auth=auth)

    maintenance_logs_data = viewIncidentMaintananceLogs(project_id, system_id, incident_id)

    if response.status_code == 200:
        data = response.json()

        # Extract the data you need from the JSON response
        context = {
            'incident_data': data,
            'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
            'maintenance_logs_data': maintenance_logs_data
            # 'occurrence_date': datetime.fromisoformat(data['OccurrenceDate'])
        }
        # Render the template and pass the context
        return render(request, 'base/viewIncident.html', context)

    else:
        message = 'Invalid Incident Credentials!'
        incident_id_form = IncidentInfoIdForm()


    # # Use get_object_or_404 to retrieve the IncidentInfo instance
    # incident = get_object_or_404(IncidentInfo, pk=pk)

    # # Access related objects with correct lowercase names
    # equipment_details = EquipmentDetails.objects.filter(
    #     incident_id=incident).first()
    # location_details = LocationDetails.objects.filter(
    #     incident_id=incident).first()
    # maintenance_info = MaintananceInfo.objects.filter(
    #     incident_id=incident).first()
    # incident_details = IncidentDetail.objects.filter(
    #     incident_id=incident).first()
    # incident_analysis = IncidentAnalysis.objects.filter(
    #     incident_id=incident).first()

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


def viewIncidentMaintananceLogs(project_id, system_id, incident_id):

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_id}/MaintenanceLogs'

    auth = (settings.API_USERNAME, settings.API_PASSWORD)

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()

        # Check if "value" property exists
        if 'value' in data:
            # Extract the "value" property
            maintenance_logs_data = data['value']
            
            # Return the "value" property as a JSON response
            return maintenance_logs_data

        else:
            return JsonResponse({'error': 'No maintenance logs available'}, status=404)
    else:
        print('logs not found')
        return JsonResponse({'error': 'Logs not found'}, status=404)    

def insert_new_record(request):
    # Add your logic here to insert a new record for the  MAINTENANCE
    # UNDER CONSTRUCTION
    # For example, you can save data to the database or perform any desired action.
    # You can customize the response as needed.
    return HttpResponse("New record inserted successfully")


def maintenanceLogCreate(request):
    # Handle form submissions if POST request
    # if request.method == 'POST':
    #     # Process the form data and create a new maintenance log record
    #     # ...

    #     # Assuming the form processing is successful, you can close the popup and update the table data
    #     return render(request, 'maintenanceLogCreate.html')
    context = {}
    # If it's not a POST request, simply render the maintenanceLogCreate.html
    return render(request, 'base/maintenanceLogCreate.html', context)
