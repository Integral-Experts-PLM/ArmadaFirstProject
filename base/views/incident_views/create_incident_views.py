import requests
import json
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from ...forms import IncidentInfoForm, EquipmentDetailsForm, LocationDetailsForm, MaintenanceInfoForm, IncidentDetailForm, IncidentAnalysisForm, IncidentInfoIdForm, IncidentCreationForm
from datetime import datetime

auth = (settings.API_USERNAME, settings.API_PASSWORD)

# def createIncidentForms(request):
#     configuration_name = request.session.get('configuration_name')
#     tree_item_name = request.session.get('tree_item_name')
#     tree_items_data = request.session.get('tree_items_data', [])
#     incident_info_form = IncidentInfoForm(request.POST or None)
#     equipment_details_form = EquipmentDetailsForm(request.POST or None)
#     location_details_form = LocationDetailsForm(request.POST or None)
#     incident_details_form = IncidentDetailForm(request.POST or None)
#     context = {
#         'configuration_name': configuration_name,
#         'tree_item_name': tree_item_name,
#         'tree_items_data': tree_items_data,
#         'incident_info_form': incident_info_form,
#         'equipment_details_form': equipment_details_form,
#         'location_details_form': location_details_form,
#         'incident_details_form': incident_details_form,
#         'view': 'create_incident_forms'
#     }
#     return render(request, 'base/createIncident.html', context)

def createIncident(request):
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    configuration_name = request.session.get('configuration_name')
    tree_item_name = request.session.get('tree_item_name')
    tree_items_data = request.session.get('tree_items_data', [])
    globalContext = request.session.get('context_data', {})
   
    # Create forms for the incident creation
    incident_info_form = IncidentInfoForm(request.POST or None)
    equipment_details_form = EquipmentDetailsForm(request.POST or None)
    location_details_form = LocationDetailsForm(request.POST or None)
    incident_details_form = IncidentDetailForm(request.POST or None)

    context = {
        'configuration_name': configuration_name,
        'tree_item_name': tree_item_name,
        'tree_items_data': tree_items_data,
        'incident_info_form': incident_info_form,
        'equipment_details_form': equipment_details_form,
        'location_details_form': location_details_form,
        'incident_details_form': incident_details_form,
        'view': 'create_incident_forms'
    }

    # Define base URL
    base_url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/'

    # Define URLs for configurations and tree items
    # url_configuration = f'{base_url}Configurations'
    # url_tree_items = f'{base_url}TreeItems'

    # Function to handle the API request and response
    # def make_api_request(url):
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Accept": "application/json",
    #     }

    #     response = requests.get(url, auth=auth)

    #     if response.status_code == 200:
    #         data = response.json()
    #         return data
    #     else:
    #         return None  # Handle errors as needed

    # # Get configuration and tree item data
    # configuration_data = make_api_request(url_configuration)
    # tree_items_data = make_api_request(url_tree_items)

    configuration_id = request.session.get('configuration_id')
    # if configuration_data is not None and tree_items_data is not None:
    if configuration_id is not None :
        # configuration = configuration_data.get('value', [])[0].get('ID')
        # tree_items = tree_items_data.get('value', [])[0].get('ID')

        if request.method == 'POST' and incident_info_form.is_valid() and equipment_details_form.is_valid() and location_details_form.is_valid() and incident_details_form.is_valid():
            tree_item_name = request.POST.get('tree_item_name', '')

            if  request.session['tree_item_id'] != '0':
                tree_item_id = request.session['tree_item_id']
            else:
                tree_item_id = request.POST.get('tree_item_id', '')

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
                # "configuration": incident_data.configuration,
                "UserText13": incident_data.user_text13_tail_number,
                "UserText17": incident_data.user_text17_mission_effect,

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

                "Configuration@odata.bind": f"Systems({system_id})/Configurations({configuration_id})",
                "SystemTreeItem@odata.bind": f"Systems({system_id})/TreeItems({tree_item_id})"
                # "SystemTreeItem@odata.bind": f"Systems({system_id})/TreeItems({equipment_data.tree_item_id})"
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
                data = response.json()
                if data:
                    data['SystemTreeItem'] = {'Name': tree_item_name}
                    request.session['incident_ID'] = data['ID']
                    # create the dictionary so incident report view has the data realted to the incident id
                    if 'incidents_dict' not in request.session:
                        request.session['incidents_dict'] = {}
                    request.session['incidents_dict'][data['ID']] = data
                    globalContext.update(data)
                    request.session['context_data'] = globalContext
                    # request.session['incidents_dict'] = {data['ID']: data}
                    # if len(globalContext['incidents_data']) == 0:
                    #     request.session['incidents_dict'] = data
                # print(f"Incident created: Date: {response.json()}")
                return redirect('incident_report')
            else:
                print(f"Failed to create incident. Status code: {response.status_code}")
                print(response.text)  # Print the response content for debugging
        else:
            # context = {
            # 'incident_info_form': incident_info_form,
            # 'equipment_details_form': equipment_details_form,
            # 'location_details_form': location_details_form,
            # 'incident_details_form': incident_details_form,
            # 'view': 'create_incident'
            # }

            context = {
            'configuration_name': configuration_name,
            'tree_item_name': tree_item_name,
            'tree_items_data': tree_items_data,
            'incident_info_form': incident_info_form,
            'equipment_details_form': equipment_details_form,
            'location_details_form': location_details_form,
            'incident_details_form': incident_details_form,
            'view': 'create_incident'
            }
    else:
        print("Failed to retrieve configuration and tree item data.")

    return render(request, 'base/createIncident.html', context)