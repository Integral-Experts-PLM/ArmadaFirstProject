import requests
from django.http import JsonResponse, HttpResponseServerError
from django.conf import settings

auth = (settings.API_USERNAME, settings.API_PASSWORD)

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
        return  HttpResponseServerError("An error occurred while fetching systems data")