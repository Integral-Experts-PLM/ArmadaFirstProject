import requests
from django.http import JsonResponse, HttpResponseServerError
from django.conf import settings
import json

auth = (settings.API_USERNAME, settings.API_PASSWORD)

# get systems to populate the dropdowns
def get_configurations(request):
    request_data = json.loads(request.body.decode('utf-8'))
    selectedProjectId = request_data.get('projectId')
    selectedSystemId = request_data.get('systemId')
    
    getConfigurationsUrl = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{selectedProjectId}/Systems({selectedSystemId})/Configurations'

    try:
        response = requests.get(getConfigurationsUrl, auth=auth)
        if response.status_code == 200:
            allConfigurationsFromProjectAndSystem = response.json()
            configurations_data = [{'ID': configuration['ID'], 'Name': configuration['ConfigurationIdentifier']} for configuration in allConfigurationsFromProjectAndSystem['value']]
            return JsonResponse({'allConfigurationsFromProjectAndSystem': configurations_data})
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return  HttpResponseServerError("An error occurred while fetching systems data")