import requests
import json
from django.conf import settings
from django.shortcuts import render, redirect
from ...forms import OperatingTimesForm

auth = (settings.API_USERNAME, settings.API_PASSWORD)

def operatingTimesCreate(request):
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    configuration_name = request.session.get('configuration_name')
    configuration_id = request.session.get('configuration_id')

    # Create forms for the incident creation
    operating_times_form = OperatingTimesForm(request.POST or None)

    context = {
        'message': None,
        'configuration_name': configuration_name,
        'operating_times_form': operating_times_form,
        'view': 'operating_times_create'
    }
    print(context['message'])
    # Define base URL
    base_url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/'

    if request.method == 'POST':
        if operating_times_form.is_valid():
            operating_times_data = operating_times_form.save(commit=False)

            # Define the URL for creating an incident
            url_post = f'{base_url}OperatingTimes'

            # Define the payload for creating an incident

            # the userText1 is causing an error
            # the userText1 MUST be a REAL valid tail number to work
            payload = {
                "Identifier": operating_times_data.identifier,
                "UserText1": operating_times_data.user_text1_tail_number,
                "StartDate": operating_times_data.start_date.strftime("%Y-%m-%dT%H:%M:%S+02:00"),
                "EndDate": operating_times_data.end_date.strftime("%Y-%m-%dT%H:%M:%S+02:00"),
                # "OperationalTime": operating_times_data.operational_time,
                "MultiplicativeAdjustment": operating_times_data.multiplicative_djustment,
                "Configuration@odata.bind": f"Systems({system_id})/Configurations({configuration_id})",
            }

            # Set the headers for the request
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            # Convert the payload dictionary to a JSON string
            payload_json = json.dumps(payload)

            print(payload_json)

            # Make the POST request to create an incident
            response = requests.post(url_post, data=payload_json, headers=headers, auth=auth)

            if response.status_code == 201:
                return redirect('operating_times')
            else:
                print(f"Failed to create operating time. Status code: {response.status_code}")
                print(response.text)
                error_data = json.loads(response.text)
                if len(error_data.get('error', {}).get('message')) > 70:
                    context['message'] = "Tail number must be a valid one!"
                else:
                    context['message'] = error_data.get('error', {}).get('message')
        else:
            print("Request or form are invalid!")
            context['message'] = "All fields are required!"

    return render(request, 'base/operatingTimes/operatingTimesCreate.html', context) 
