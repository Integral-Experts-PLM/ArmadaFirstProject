import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from .maintenanceLogs_views import maintenanceLogs

auth = (settings.API_USERNAME, settings.API_PASSWORD)
# auth = ('fksdjñl', settings.API_PASSWORD)

def viewAllIncidents(request):
    # project_id = request.session.get('project_id')
    # system_id = request.session.get('system_id')
    # configuration_id = request.session.get('configuration_id')
    # tree_item_id = request.session.get('tree_item_id')
    incident_ID = None

    if request.method == 'POST':
        # Get the selected incident ID from the POST request
        incident_ID = request.body.decode('utf-8')
        request.session['incident_ID'] = incident_ID
    else:
        # If not a POST request, use the session variable as the initial selected incident ID
        incident_ID = request.session.get('incident_ID', 'default-incident-id')
    
    context = request.session.get('context_data', {})

    if len(context['incidents_data']) > 0:
        context['selectedIncidentId'] = incident_ID
    else:
        print('no incidents found')

    
    return render(request, 'base/view_incidents/viewAllIncidents.html', context)
    # url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents?$expand=Configuration,SystemTreeItem'
    # response = requests.get(url, auth=auth)
    # if response.status_code == 200:
    #     filtered_incidents = None
    #     data = response.json()
    #     allIncidents = data['value']
    #     if tree_item_id != '0':
    #         filtered_incidents = [incident for incident in allIncidents if incident['Configuration'].get('ID') == int(configuration_id) and incident['SystemTreeItem'].get('ID') == int(tree_item_id)]
    #     else:
    #         filtered_incidents = [incident for incident in allIncidents if incident['Configuration'].get('ID') == int(configuration_id)]
    #     context = {
    #         'incidents_data': filtered_incidents,
    #         'page': 'view-all-incidents',
    #         'selectedIncidentId': incident_ID,
    #     }
    # else:
    #     return


def viewIncidentReport(request):
    message = None
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.session.get('incident_ID')

    maintenance = maintenanceLogs(request)

    globalContext = request.session.get('context_data', {})

    if len(globalContext['incidents_data']) > 0:
        url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}?$expand=Configuration,SystemTreeItem'
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            data = response.json()
        else:
            return JsonResponse({'error': 'Incident not found'}, status=404)
        context = {
            'incident_data': data,
            'configuration_id': data['Configuration']['ConfigurationIdentifier'],
            'tree_item_id': data['SystemTreeItem']['SystemTreeIdentifier'],
            'OccurrenceDate': data['OccurrenceDate'].split('T')[0],
            'maintenance_logs_data': maintenance['maintenance_logs_data'],
            'maintenance_logs_message': maintenance['message'],
            'page': 'incident-report',
            # 'occurrence_date': datetime.fromisoformat(data['OccurrenceDate'])
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

    globalContext = request.session.get('context_data', {})

    if len(globalContext['incidents_data']) > 0:
        url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}?$expand=Configuration,SystemTreeItem'

        response = requests.get(url, auth=auth)

        if response.status_code == 200:
            data = response.json()
        else:
            return JsonResponse({'error': 'Incident not found'}, status=404)
        
        context = {
            'incident_data': data,
            'configuration_id': data['Configuration']['ConfigurationIdentifier'],
            'tree_item_id': data['SystemTreeItem']['SystemTreeIdentifier'],
            'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
            # 'occurrence_date': datetime.fromisoformat(data['OccurrenceDate'])
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

    globalContext = request.session.get('context_data', {})

    if len(globalContext['incidents_data']) > 0:
        url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}?$expand=Configuration,SystemTreeItem'

        response = requests.get(url, auth=auth)

        if response.status_code == 200:
            data = response.json()
        else:
            return JsonResponse({'error': 'Incident not found'}, status=404)
        
        context = {
            'incident_data': data,
            'configuration_id': data['Configuration']['ConfigurationIdentifier'],
            'tree_item_id': data['SystemTreeItem']['SystemTreeIdentifier'],
            'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
            # 'occurrence_date': datetime.fromisoformat(data['OccurrenceDate'])
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

    maintenace = maintenanceLogs(request)

    globalContext = request.session.get('context_data', {})

    if len(globalContext['incidents_data']) > 0:
        url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}?$expand=Configuration,SystemTreeItem'

        response = requests.get(url, auth=auth)

        if response.status_code == 200:
            data = response.json()
        else:
            return JsonResponse({'error': 'Incident not found'}, status=404)
        
        context = {
            'incident_data': data,
            'configuration_id': data['Configuration']['ConfigurationIdentifier'],
            'tree_item_id': data['SystemTreeItem']['SystemTreeIdentifier'],
            'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
            # 'occurrence_date': datetime.fromisoformat(data['OccurrenceDate'])
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

