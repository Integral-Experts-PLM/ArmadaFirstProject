import requests
from django.http import JsonResponse, HttpResponseServerError
from django.conf import settings
import json

auth = (settings.API_USERNAME, settings.API_PASSWORD)

# get systems to populate the dropdowns
def get_tree_items(request):
    request_data = json.loads(request.body.decode('utf-8'))
    selectedProjectId = request_data.get('projectId')
    selectedSystemId = request_data.get('systemId')
    selectedConfigurationId = request_data.get('configurationId')
    
    getSystemTreeItemUrl = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{selectedProjectId}/Systems({selectedSystemId})/Configurations({selectedConfigurationId})/SystemTreeItems?$select=ID,ParentID,Name'

    try:
        response = requests.get(getSystemTreeItemUrl, auth=auth)
        if response.status_code == 200:
            allTreeItemsFromProjectSystemConfiguration = response.json()
            tree_items_data = [{'ID': treeItem['ID'], 'Name': treeItem['Name']} for treeItem in allTreeItemsFromProjectSystemConfiguration['value']]
            # Prepend the default item "All Items"
            tree_items_data.insert(0, {'ID': 0, 'Name': 'All Items'})
            request.session['tree_items_data'] = tree_items_data[1:] #in the session we only want the items names

            return JsonResponse({'allTreeItemsFromProjectSystemConfiguration': tree_items_data})
        elif response.status_code == 400:
            return JsonResponse({'allTreeItemsFromProjectSystemConfiguration': None})
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return  HttpResponseServerError("An error occurred while fetching systems data")
    