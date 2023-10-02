from django.http import JsonResponse
import requests

def api_request_view(request):
    url = 'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/ProjectMgmt/Projects'
    username = 'your_username'
    password = 'your_password'

    auth = (username, password)

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
        # Process the data
        return JsonResponse(data)
    else:
        error_message = f"Request failed with status code {response.status_code}: {response.text}"
        return JsonResponse({"error": error_message}, status=500)
