import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from ..maintenanceLogs_views import maintenanceLogs

auth = (settings.API_USERNAME, settings.API_PASSWORD)

def viewAllIncidents(request):
    incident_ID = None

    # if request.method == 'POST':
    #     # Get the selected incident ID from the POST request
    #     incident_ID = request.body.decode('utf-8')
    #     request.session['incident_ID'] = incident_ID
    # else:
    #     # If not a POST request, use the session variable as the initial selected incident ID
    #     incident_ID = request.session.get('incident_ID', 'default-incident-id')
        # If not a POST request, use the session variable as the initial selected incident ID
    incident_ID = request.session.get('incident_ID', 'default-incident-id')
    
    globalContext = request.session.get('context_data', {})

    if len(globalContext['incidents_data']) > 0:
        globalContext['selectedIncidentId'] = incident_ID
    else:
        print('no incidents found')
    
    return render(request, 'base/view_incidents/viewAllIncidents.html', globalContext)

def getIncidentData(request):
    if request.method == 'POST':
        # Get the selected incident ID from the POST request
        incident_ID = request.body.decode('utf-8')

        request.session['incident_ID'] = incident_ID
        globalContext = request.session.get('context_data', {})
        globalContext['selectedIncidentId'] = incident_ID
        json_data = globalContext['incidents_data']
        return JsonResponse(json_data, safe=False) # Set safe to False for non-dict objects


def viewIncidentReport(request):
    message = None
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.session.get('incident_ID')
    configuration_name = request.session.get('configuration_name')
    maintenance = maintenanceLogs(request)
    globalContext = request.session.get('context_data', {})
    incidents_dict = request.session.get('incidents_dict', {})

    if len(globalContext['incidents_data']) > 0:
        # url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}?$expand=Configuration,SystemTreeItem'
        # response = requests.get(url, auth=auth)
        # if response.status_code == 200:
        #     data = response.json()
        # else:
        #     return JsonResponse({'error': 'Incident not found'}, status=404)

        data = incidents_dict.get(incident_ID)
        
        context = {
            'incident_data': data,
            'incident_ID': incident_ID,
            'configuration_name': configuration_name,
            'tree_item_name': data['SystemTreeItem']['SystemTreeIdentifier'],
            'OccurrenceDate': data['OccurrenceDate'].split('T')[0],
            'maintenance_logs_data': maintenance['maintenance_logs_data'],
            'maintenance_logs_message': maintenance['message'],
            'page': 'incident-report',
        }
    else:
        context = {
            'message': 'There are no FRACAS Incidents',
            'page': 'incident-report',
        }

    return render(request, 'base/incidentReport.html', context) 


def viewAnalysis(request):
    message = None
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.session.get('incident_ID')
    configuration_name = request.session.get('configuration_name')
    globalContext = request.session.get('context_data', {})
    incidents_dict = request.session.get('incidents_dict', {})

    if len(globalContext['incidents_data']) > 0:
        # url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}?$expand=Configuration,SystemTreeItem'

        # response = requests.get(url, auth=auth)

        # if response.status_code == 200:
        #     data = response.json()
        # else:
        #     return JsonResponse({'error': 'Incident not found'}, status=404)

        data = incidents_dict.get(incident_ID)
        
        context = {
            'incident_data': data,
            'configuration_name': configuration_name,
            'tree_item_name': data['SystemTreeItem']['SystemTreeIdentifier'],
            'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
            'page': 'analysis',
        }
    else:
        context = {
            'message': 'There are no FRACAS Incidents',
            'page': 'incident-report',
        }

    return render(request, 'base/analysis.html', context) 


def viewReviewBoard(request):
    message = None
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.session.get('incident_ID')
    configuration_name = request.session.get('configuration_name')
    globalContext = request.session.get('context_data', {})
    incidents_dict = request.session.get('incidents_dict', {})

    if len(globalContext['incidents_data']) > 0:
        # url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}?$expand=Configuration,SystemTreeItem'

        # response = requests.get(url, auth=auth)

        # if response.status_code == 200:
        #     data = response.json()
        # else:
        #     return JsonResponse({'error': 'Incident not found'}, status=404)

        data = incidents_dict.get(incident_ID)
        
        context = {
          'incident_data': data,
            'configuration_name': configuration_name,
            'tree_item_name': data['SystemTreeItem']['SystemTreeIdentifier'],
            'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
            'page': 'review-board',
        }
    else:
        context = {
            'message': 'There are no FRACAS Incidents',
            'page': 'incident-report',
        }

    return render(request, 'base/reviewBoard.html', context) 


def viewOverview(request):
    message = None
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.session.get('incident_ID')
    configuration_name = request.session.get('configuration_name')
    maintenace = maintenanceLogs(request)
    globalContext = request.session.get('context_data', {})
    incidents_dict = request.session.get('incidents_dict', {})

    if len(globalContext['incidents_data']) > 0:
        # url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}?$expand=Configuration,SystemTreeItem'

        # response = requests.get(url, auth=auth)

        # if response.status_code == 200:
        #     data = response.json()
        # else:
        #     return JsonResponse({'error': 'Incident not found'}, status=404)

        data = incidents_dict.get(incident_ID)
        
        context = {
            'incident_data': data,
            'incident_ID': incident_ID,
            'configuration_name': configuration_name,
            'tree_item_name': data['SystemTreeItem']['SystemTreeIdentifier'],
            'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
            'maintenance_logs_data': maintenace['maintenance_logs_data'],
            'maintenance_logs_message': maintenace['message'],
            'page': 'overview',
        }
    else:
        context = {
            'message': 'There are no FRACAS Incidents',
            'page': 'incident-report',
        }

    return render(request, 'base/overview.html', context) 
