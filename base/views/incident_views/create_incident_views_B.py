import requests
import json
from datetime import datetime
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from ...forms import CreateIncidentForm, IncidentInfoForm, EquipmentDetailsForm, LocationDetailsForm, MaintenanceInfoForm, IncidentDetailForm, IncidentAnalysisForm, IncidentInfoIdForm, IncidentCreationForm
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

def createIncident_B(request):
    project_id = request.session.get('project_id')
    project_name = request.session.get('project_name')
    system_id = request.session.get('system_id')
    system_name = request.session.get('system_name')
    configuration_name = request.session.get('configuration_name')
    tree_item_name = request.session.get('tree_item_name')
    tree_items_data = request.session.get('tree_items_data', [])
   
    # Create forms for the incident creation
    # incident_info_form = IncidentInfoForm(request.POST or None)
    # equipment_details_form = EquipmentDetailsForm(request.POST or None)
    # location_details_form = LocationDetailsForm(request.POST or None)
    # incident_details_form = IncidentDetailForm(request.POST or None)
    create_incident_form = CreateIncidentForm(request.POST or None)

    context = {
        'configuration_name': configuration_name,
        'tree_item_name': tree_item_name,
        'tree_items_data': tree_items_data,
        'create_incident_form': create_incident_form,
        # 'incident_info_form': incident_info_form,
        # 'equipment_details_form': equipment_details_form,
        # 'location_details_form': location_details_form,
        # 'incident_details_form': incident_details_form,
        'view': 'create_incident_forms'
    }

    # Define base URL
    base_url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/'

    configuration_id = request.session.get('configuration_id')
    if configuration_id is not None :
        print(create_incident_form.is_valid())
        if request.method == 'POST'and create_incident_form.is_valid():
        
        # and incident_info_form.is_valid() and equipment_details_form.is_valid() and location_details_form.is_valid() and incident_details_form.is_valid():
            tree_item_name = request.POST.get('tree_item_name', '')

            if  request.session['tree_item_id'] != '0':
                tree_item_id = request.session['tree_item_id']
            else:
                tree_item_id = request.POST.get('tree_item_id', '')

            # incident_data = incident_info_form.save(commit=False)
            # equipment_data = equipment_details_form.save(commit=False)
            # location_details = location_details_form.save(commit=False)
            # incident_details = incident_details_form.save(commit=False)
            create_incident_details = create_incident_form.save(commit=False)
            # Define the URL for creating an incident
            url_post = f'{base_url}Incidents'

            # hour = request.POST.get('occurrence_time')
            # Define the payload for creating an incident
            payload = {
                "UserText22": create_incident_details.user_text22_failure_detection_situation,
                "UserText23": create_incident_details.user_text23_failure_buque_situation,
                "UserText24": create_incident_details.user_text24_failure_effect_item,
                "UserText25": create_incident_details.user_text25_failure_evidence,
                "OccurrenceDate": create_incident_details.occurrence_date.strftime("%Y-%m-%dT%H:%M:%S+01:00"),
                # "OccurrenceTime": hour,
                "DescriptionIncident": create_incident_details.description_incident,
                


                # "OccurrenceDate": create_incident_details.occurrence_date.strftime("%Y-%m-%dT%H:%M:%S+01:00"),
                # "OccurrenceTime": create_incident_details.occurrence_date.strftime("%Y-%m-%dT%H:%M:%S+01:00"),

                # "PersonIncidentEntry": incident_data.person_incident_entry,
                # "OccurrenceDate": incident_data.occurrence_date.strftime("%Y-%m-%dT%H:%M:%S+01:00"),
                # "UserText13": incident_data.user_text13_tail_number,
                # "UserText17": incident_data.user_text17_mission_effect,

                # "SerialNumber": equipment_data.serial_number,
                # "MeterReading": equipment_data.meter_reading_tsn,
                # "TimeToFailure": equipment_data.time_to_failure_tso,
                # "UserText10": equipment_data.user_text10_oem,
                # "UserText11": equipment_data.analysis_team,

                # "UserText4": location_details.user_text4_location,
                # "UserText23": location_details.user_text24_address,
                # "UserText25": location_details.user_text25_contact,
                # "UserText22": location_details.user_text22_phone,
                # "UserText21": location_details.user_text21_email,

                # "OperatingMode": incident_details.operating_mode,
                # "UserText2": incident_details.user_text2_initial_severity,
                # "DescriptionIncident": incident_details.description_incident,
                # attachments are getting error. in relex is the type of string but here supose to be file - further review
                # "AttachmentsIncidents": incident_details.attachments_incidents,

                "Configuration@odata.bind": f"Systems({system_id})/Configurations({configuration_id})",
                "SystemTreeItem@odata.bind": f"Systems({system_id})/TreeItems({tree_item_id})"
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
            print(payload_json)
            # Check the response
            if response.status_code == 201:
                data = response.json()
                if data:
                    data['SystemTreeItem'] = {'Name': tree_item_name}
                    request.session['incident_ID'] = data['ID']
                    if 'incidents_dict' not in request.session:
                        request.session['incidents_dict'] = {}

                    request.session['incidents_dict'][data['ID']] = data
                    request.session['context_data']['incidents_data'].append(data)
                return redirect('incident_report')
            else:
                print(f"Failed to create incident. Status code: {response.status_code}")
                print(response.text)  # Print the response content for debugging
        else:
            context = {
            'project_name': project_name,
            'system_name': system_name,
            'configuration_name': configuration_name,
            'tree_item_name': tree_item_name,
            'tree_items_data': tree_items_data,
            'create_incident_form': create_incident_form,

            # 'incident_info_form': incident_info_form,
            # 'equipment_details_form': equipment_details_form,
            # 'location_details_form': location_details_form,
            # 'incident_details_form': incident_details_form,
            'view': 'create_incident_B'
            }
    else:
        print("Failed to retrieve configuration and tree item data.")

    return render(request, 'base/createIncident.html', context)