import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render

auth = (settings.API_USERNAME, settings.API_PASSWORD)

def viewOperatingTimes(request):
    message = None
    project_id = request.session.get('project_id')
    system_id = request.session.get('system_id')
    url = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{project_id}/Systems({system_id})/OperatingTimes'

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
        # Check if "value" property exists
        if 'value' in data:
            # Extract the "value" property
            operating_times = data['value']
        else:
            message = 'This incident has no operating times yet!'
    else:
        return JsonResponse({'error': 'Operating times not found'}, status=404)
    context = {
        'operating_times': operating_times,
        'message': message,
        'page': 'operating-times',
    }
    return render(request, 'base/operatingTimes/operatingTimes.html', context) 
