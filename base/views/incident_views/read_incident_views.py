import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from ..maintenanceLogs_views import maintenanceLogs
from datetime import datetime
from ...db_queries import get_all_incidents, get_tree_name
from ...web_services import get_projects
from django.core.paginator import Paginator
from ...templatetags.custom_filters import format_datetime
import re

auth = (settings.API_USERNAME, settings.API_PASSWORD)

def search_incidents(request, message=None):
    # message = None
    allProjects = get_projects()
    context = {'allProjects': allProjects, 'message': message}
    return render(request, 'base/incidents/search_incidents.html', context)
    
def view_incidents(request):
    if request.method == 'POST':
        set_id = request.POST.get('system_id')
        configuration_id = request.POST.get('configuration_id')
        tree_id = request.POST.get('tree_item_id')
        request.session['FR_set_id'] = set_id
        # request.session['project_name'] = project_name
        # request.session['system_id'] = system_id
        # request.session['system_name'] = system_name
        request.session['FR_configuration_id'] = configuration_id
        # request.session['configuration_name'] = configuration_name
        # request.session['tree_item_id'] = tree_item_id
        # request.session['tree_item_name'] = tree_item_name
    else:
        set_id = request.session.get('FR_set_id')
        configuration_id = request.session.get('FR_configuration_id')
        tree_id = request.session.get('FR_tree_item_id')

    # Recoger parámetros de filtrado
    filter_column = request.GET.get('filter_column')
    filter_value = request.GET.get('filter_value')

    if request.session.get('FR_set_id') :
        incidents_data = get_all_incidents(set_id, configuration_id, tree_id)
        if incidents_data is None:
            incidents_data = [] # para que incidents_data siempre sea una secuencia iterable incluso si está vacía antes de pasarla al Paginator. 
       
        # Añadir el nombre del TreeItem a cada incidencia
        for incident in incidents_data:
            incident.TreeName = incident.TreeID.Name

        # Filtrar incidents_data basándose en filter_column y filter_value
        if filter_column and filter_value:
            incidents_data = filter_incidents(incidents_data, filter_column, filter_value)

        paginator = Paginator(incidents_data, 50)  # 50 incidentes por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        start_number = (page_obj.number - 1) * 50
        context = {'page_obj': page_obj, 'start_number': start_number}
        return render(request, 'base/incidents/view_incidents.html', context)
    else:
        message = 'Clase y Serie son campos obligatorios'
        return search_incidents(request, message=message)
    
def filter_incidents(incidents, column, value):
    filtered_incidents = []

    for incident in incidents:
        attribute_value = getattr(incident, column, None)

        # Comprobar si el atributo es una instancia de datetime
        if isinstance(attribute_value, datetime):
            # Formatear la fecha y comparar
            if format_datetime(attribute_value) == value:
                filtered_incidents.append(incident)
        else:
            pattern = r'~[^:]+:.+'  # Patrón para ~texto:texto (~SEVERITY:CRITICAL)
            if isinstance(attribute_value, str) and re.match(pattern, attribute_value):
                # Tomar el texto después de los dos puntos
                attribute_value = attribute_value.split(':', 1)[1]

            # Para otros tipos de datos, realizar una comparación directa
            if str(attribute_value).lower() == value.lower():
                filtered_incidents.append(incident)

    return filtered_incidents





####################################################
####################################################

def viewAllIncidents(request):
    incident_ID = None
    incident_ID = request.session.get('incident_ID', 'default-incident-id')
    globalContext = request.session.get('context_data', {})

    if globalContext['incidents_data'] != None:
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
        data = incidents_dict.get(str(incident_ID))
        context = {
            'incident_data': data,
            'incident_ID': incident_ID,
            'configuration_name': configuration_name,
            'tree_item_name': data['SystemTreeItem']['Name'],
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
        data = incidents_dict.get(str(incident_ID))
        context = {
            'incident_data': data,
            'configuration_name': configuration_name,
            'tree_item_name': data['SystemTreeItem']['Name'],
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
        data = incidents_dict.get(str(incident_ID))
        context = {
          'incident_data': data,
            'configuration_name': configuration_name,
            'tree_item_name': data['SystemTreeItem']['Name'],
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
        data = incidents_dict.get(str(incident_ID))
        context = {
            'incident_data': data,
            'incident_ID': incident_ID,
            'configuration_name': configuration_name,
            'tree_item_name': data['SystemTreeItem']['Name'],
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
