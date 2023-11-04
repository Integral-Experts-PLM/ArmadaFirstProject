import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render

auth = (settings.API_USERNAME, settings.API_PASSWORD)

def viewMaintenanceLogs(request):
    maintenance = maintenanceLogs(request)
    # incident_ID = request.session.get('incident_ID')
    
    # if not len(maintenance['maintenance_logs_data']):
    #     message = "There are no maintenance logs yet!"

    context = {
        'maintenance_logs_data': maintenance['maintenance_logs_data'],
        'incident_ID':  maintenance['incident_ID'],
        'message': maintenance['message'],
        'page': 'maintenance-logs',
    }
    # return render(request, 'base/maintenanceLogs.html', context) 
    return render(request, 'base/maintenance_logs/maintenance_logs.html', context) 

def maintenanceLogs(request):
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.session.get('incident_ID')

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}/MaintenanceLogs'

    context = {
        'maintenance_logs_data': None,
        'incident_ID': incident_ID,
        'message': None,
    }

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
        # Check if "value" property exists
        if 'value' in data:
            # Extract the "value" property
            context['maintenance_logs_data'] = data['value']
        else:
            return JsonResponse({'error': 'There is no "value" on this data'}, status=404)
        
        if not len(context['maintenance_logs_data']):
            context['message'] = "There are no maintenance logs yet!"
    else:
        return JsonResponse({'error': 'No maintenance logs available'}, status=404)
    return context