import pprint
import json
from django.http import JsonResponse
from django.conf import settings
import requests
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import IncidentInfo, EquipmentDetails, LocationDetails, MaintenanceInfo, IncidentDetail, IncidentAnalysis
from .forms import IncidentInfoForm, EquipmentDetailsForm, LocationDetailsForm, MaintenanceInfoForm, IncidentDetailForm, IncidentAnalysisForm, IncidentInfoIdForm, IncidentCreationForm
from datetime import datetime

# global credentials to be used on all calls
auth = (settings.API_USERNAME, settings.API_PASSWORD)


# get projects to populate the dropdowns
def get_projects():
    getProjectsUrl = 'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/ProjectMgmt/Projects'
    try:
        response = requests.get(getProjectsUrl, auth=auth)
        if response.status_code == 200:
            allProjects = response.json()
            return allProjects
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

# get systems to populate the dropdowns
def get_systems(request):
    selectedProjectId = request.body.decode('utf-8')
    
    getSystemsUrl = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{selectedProjectId}/Systems'

    try:
        response = requests.get(getSystemsUrl, auth=auth)
        if response.status_code == 200:
            allSystemsFromProject = response.json()
            systems_data = [{'ID': system['ID'], 'Name': system['Name']} for system in allSystemsFromProject['value']]
            return JsonResponse({'allSystemsFromProject': systems_data})
        else:
            print(selectedProjectId)
            print(f"Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# get incidents to populate the dropdowns
def get_incidents(request):
    data = json.loads(request.body.decode('utf-8'))
    selectedProjectId = data.get('selectedProjectId')
    selectedSystemId = data.get('selectedSystemId')

    getIncidentsUrl = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{selectedProjectId}/Systems({selectedSystemId})/Incidents'

    try:
        response = requests.get(getIncidentsUrl, auth=auth)
        if response.status_code == 200:
            allIncidentsFromSystem = response.json()
            incidents_data = [{'ID': incident['ID']} for incident in allIncidentsFromSystem['value']]
            return JsonResponse({'allIncidentsFromSystem': incidents_data})
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def home(request):
    message = None  # Initialize the message variable
    allProjects = get_projects()

    if request.method == 'POST':
        # You can now use selectedProjectId as needed in your view
        project_id = request.POST.get('project_id')
        system_id = request.POST.get('system_id')

        if project_id and system_id:
            url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/'

            response = requests.get(url, auth=auth)
            if response.status_code == 200:
                # Store the values in the session
                request.session['project_id'] = project_id
                request.session['system_id'] = system_id
                return redirect('view_all_incidents')
            else:
                message = 'Invalid Incident Credentials!'
        else:
            message = 'All Fields Are Required!'

    context = {'message': message, 'allProjects': allProjects}
    return render(request, 'base/home.html', context)


def homeCreateIncident(request):
    message = None  # Initialize the message variable
    allProjects = get_projects()

    if request.method == 'POST':
        # You can now use selectedProjectId as needed in your view
        project_id = request.POST.get('project_id')
        system_id = request.POST.get('system_id')

        url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents'

        response = requests.get(url, auth=auth)

        if response.status_code == 200:
            return redirect('create_incident', project_id=project_id, system_id=system_id)
        else:
            message = 'Invalid Credentials!'
    else:
        message = 'All Fields Are Required!'

    context = {'message': message, 'allProjects': allProjects}
    return render(request, 'base/homeCreate.html', context)


def createIncident(request, project_id, system_id):
    # Create forms for the incident creation
    incident_info_form = IncidentInfoForm(request.POST or None)
    equipment_details_form = EquipmentDetailsForm(request.POST or None)
    location_details_form = LocationDetailsForm(request.POST or None)
    incident_details_form = IncidentDetailForm(request.POST or None)

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
                "PersonIncidentEntry": incident_data.person_incident_entry,
                "OccurrenceDate": incident_data.occurrence_date.strftime("%Y-%m-%dT%H:%M:%S+02:00"),
                # I believe this configuration is the relation with the outside configuration - further review
                # "configuration": incident_data.configuration,
                "UserText13": incident_data.user_text13_tail_number,
                "UserText17": incident_data.user_text17_mission_effect,

                # I believe this systemTreeItem is the relation with the outside systemTreeItem - further review
                # "SystemTreeItem": equipment_data.failed_component,
                "SerialNumber": equipment_data.serial_number,
                "MeterReading": equipment_data.meter_reading_tsn,
                "TimeToFailure": equipment_data.time_to_failure_tso,
                "UserText10": equipment_data.user_text10_oem,
                "UserText11": equipment_data.analysis_team,

                "UserText4": location_details.user_text4_location,
                "UserText23": location_details.user_text24_address,
                "UserText25": location_details.user_text25_contact,
                "UserText22": location_details.user_text22_phone,
                "UserText21": location_details.user_text21_email,

                "OperatingMode": incident_details.operating_mode,
                "UserText2": incident_details.user_text2_initial_severity,
                "DescriptionIncident": incident_details.description_incident,
                # attachments are getting error. in relex is the type of string but here supose to be file - further review
                # "AttachmentsIncidents": incident_details.attachments_incidents,

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
                return redirect('view_all_incidents', project_id=project_id, system_id=system_id, incident_ID=response.json().get('ID'))
            else:
                print(f"Failed to create incident. Status code: {response.status_code}")
                print(response.text)  # Print the response content for debugging
        else:
            print('incident form not ok', incident_info_form, equipment_details_form, location_details_form, incident_details_form)
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


def deleteIncident(request, pk):
    # Use get_object_or_404 to retrieve the IncidentInfo instance
    incident = get_object_or_404(IncidentInfo, pk=pk)

    if request.method == 'POST':
        incident.delete()
        return redirect('home')

    context = {'incident': incident, 'view': 'delete_incident', }
    return render(request, 'base/deleteIncident.html', context)


def viewAllIncidents(request):
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')

    if request.method == 'POST':
        # Get the selected incident ID from the POST request
        incident_ID = request.body.decode('utf-8')
        request.session['incident_ID'] = incident_ID
        print('Selected incident ID from front: ', incident_ID)
    else:
        # If not a POST request, use the session variable as the initial selected incident ID
        incident_ID = request.session.get('incident_ID', 'default-incident-id')

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/'

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()

        # Extract the data you need from the JSON response
        context = {
            'incidents_data': data['value'],
            'page': 'view-all-indicents',
            'selectedIncidentId': incident_ID,  # Pass the current selected incident ID to the template
        }
        # Render the template and pass the context
        return render(request, 'base/viewAllIncidents.html', context)
    else:
        message = 'No incidents found!'


def viewIncident(request):
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.session.get('incident_ID')

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}'

    response = requests.get(url, auth=auth)

    maintenance_logs_data = incidentMaintenanceLogs(project_id, system_id, incident_ID)

    if response.status_code == 200:
        data = response.json()

        # Extract the data you need from the JSON response
        context = {
            'incident_data': data,
            'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
            'maintenance_logs_data': maintenance_logs_data,
            # 'occurrence_date': datetime.fromisoformat(data['OccurrenceDate'])
        }
        # Render the template and pass the context
        return render(request, 'base/viewIncident.html', context)

    else:
        message = 'Invalid Incident Credentials!'
        incident_ID_form = IncidentInfoIdForm()


# def viewIncident(request):
#     project_id = request.session.get('project_id')
#     system_id = request.session.get('system_id')
#     incident_ID = request.session.get('incident_ID')

#     url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}'

#     response = requests.get(url, auth=auth)

#     maintenance_logs_data = incidentMaintenanceLogs(project_id, system_id, incident_ID)

#     if response.status_code == 200:
#         data = response.json()

#         # Extract the data you need from the JSON response
#         context = {
#             'incident_data': data,
#             'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
#             'maintenance_logs_data': maintenance_logs_data,
#             # 'occurrence_date': datetime.fromisoformat(data['OccurrenceDate'])
#         }
#         # Render the template and pass the context
#         return render(request, 'base/viewIncident.html', context)

#     else:
#         message = 'Invalid Incident Credentials!'
#         incident_ID_form = IncidentInfoIdForm()


def viewMaintenanceLogs(request):
    message = None
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.session.get('incident_ID')

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}/MaintenanceLogs'


    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
        # Check if "value" property exists
        if 'value' in data:
            # Extract the "value" property
            maintenance_logs_data = data['value']
        else:
            message = 'This incident has no maintenance logs yet!'
    else:
        return JsonResponse({'error': 'Logs not found'}, status=404)
    context = {
        'maintenance_logs_data': maintenance_logs_data,
        'message': message,
        'page': 'maintenance-logs',
    }
    return render(request, 'base/maintenanceLogs.html', context) 


def viewOperatingTimes(request):
    message = None
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/OperatingTimes'


    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
        # Check if "value" property exists
        if 'value' in data:
            # Extract the "value" property
            operating_times = data['value']
        else:
            message = 'This incident has no operating times yet!'
    else:
        return JsonResponse({'error': 'Operating times not found'}, status=404)
    context = {
        'operating_times': operating_times,
        'message': message,
        'page': 'operating-times',
    }
    return render(request, 'base/operatingTimes.html', context) 


def viewIncidentReport(request):
    message = None
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.session.get('incident_ID')

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}'

    response = requests.get(url, auth=auth)

    maintenance_logs_data = incidentMaintenanceLogs(project_id, system_id, incident_ID)

    if response.status_code == 200:
        data = response.json()
    else:
        return JsonResponse({'error': 'Incident not found'}, status=404)
    
    context = {
        'incident_data': data,
        'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
        # 'occurrence_date': datetime.fromisoformat(data['OccurrenceDate'])
        'maintenance_logs_data': maintenance_logs_data,
        'message': message,
        'page': 'incident-report',
    }
    return render(request, 'base/incidentReport.html', context) 


def viewAnalysis(request):
    message = None
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.session.get('incident_ID')

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}'

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
    else:
        return JsonResponse({'error': 'Incident not found'}, status=404)
    
    context = {
        'incident_data': data,
        'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
        # 'occurrence_date': datetime.fromisoformat(data['OccurrenceDate'])
        'message': message,
        'page': 'analysis',
    }
    return render(request, 'base/analysis.html', context) 


def viewReviewBoard(request):
    message = None
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.session.get('incident_ID')

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}'

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
    else:
        return JsonResponse({'error': 'Incident not found'}, status=404)
    
    context = {
        'incident_data': data,
        'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
        # 'occurrence_date': datetime.fromisoformat(data['OccurrenceDate'])
        'message': message,
        'page': 'review-board',
    }
    return render(request, 'base/reviewBoard.html', context) 


def viewOverview(request):
    message = None
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.session.get('incident_ID')

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}'

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
    else:
        return JsonResponse({'error': 'Incident not found'}, status=404)
    
    context = {
        'incident_data': data,
        'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
        # 'occurrence_date': datetime.fromisoformat(data['OccurrenceDate'])
        'message': message,
        'page': 'overview',
    }
    return render(request, 'base/overview.html', context) 


def incidentMaintenanceLogs(project_id, system_id, incident_ID):

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}/MaintenanceLogs'


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
