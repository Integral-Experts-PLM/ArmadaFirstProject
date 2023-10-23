import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from .maintenanceLogs_views import maintenanceLogs

auth = (settings.API_USERNAME, settings.API_PASSWORD)
# auth = ('fksdjñl', settings.API_PASSWORD)

def viewAllIncidents(request):
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')

    if request.method == 'POST':
        # Get the selected incident ID from the POST request
        incident_ID = request.body.decode('utf-8')
        request.session['incident_ID'] = incident_ID
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
        return render(request, 'base/view_incidents/viewAllIncidents.html', context)
    else:
        message = 'No incidents found!'


def viewIncidentReport(request):
    message = None
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    incident_ID = request.session.get('incident_ID')

    maintenace = maintenanceLogs(request)

    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/{incident_ID}'

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
    else:
        return JsonResponse({'error': 'Incident not found'}, status=404)
    
    context = {
        'incident_data': data,
        'OccurrenceDate': data.get('OccurrenceDate').split('T')[0],
        'maintenance_logs_data': maintenace['maintenance_logs_data'],
        'maintenance_logs_message': maintenace['message'],
        'message': message,
        'page': 'incident-report',
        # 'occurrence_date': datetime.fromisoformat(data['OccurrenceDate'])
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

    maintenace = maintenanceLogs(request)

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
        'maintenance_logs_data': maintenace['maintenance_logs_data'],
        'maintenance_logs_message': maintenace['message'],
        'message': message,
        'page': 'overview',
    }
    return render(request, 'base/overview.html', context) 

