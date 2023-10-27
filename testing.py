def viewAllIncidents(request):
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    configuration_id = int(request.session.get('configuration_id'))
    tree_item_id = request.session.get('tree_item_id')

    if request.method == 'POST':
        # Get the selected incident ID from the POST request
        incident_ID = request.body.decode('utf-8')
        request.session['incident_ID'] = incident_ID
    else:
        # If not a POST request, use the session variable as the initial selected incident ID
        incident_ID = request.session.get('incident_ID', 'default-incident-id')

    url = None
    if tree_item_id != 0:
        url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents/$expand=Configuration($select=ID),TreeItems
    else :
        url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/Incidents?$expand=Configuration'

/Project_<projectID>/Systems(<systemID>)/FMEAs?$expand=TreeItems($select=ID,SystemTreeIdentifier)

    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        data = response.json()
        allIncidents = data['value']

        if tree_item_id != 0:
            print('not all incidents')
            filtered_incidents = [incident for incident in allIncidents if incident['SystemTreeItems'].get('ID') == tree_item_id]
        else:
            print('it is all incidents')
            filtered_incidents = [incident for incident in allIncidents if incident['Configuration'].get('ID') == configuration_id]

        context = {
            'incidents_data': filtered_incidents,
            'page': 'view-all-incidents',
            'selectedIncidentId': incident_ID,  # Pass the current selected incident ID to the template
        }
        return render(request, 'base/view_incidents/viewAllIncidents.html', context)
    else:
        message = 'No incidents found!'
