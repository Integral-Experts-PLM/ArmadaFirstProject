import requests
from django.http import JsonResponse, HttpResponseServerError
from django.conf import settings
from django.shortcuts import render
import json

auth = (settings.API_USERNAME, settings.API_PASSWORD)

def treeItemsCreate(request):
    tree_items_form_data = 'data to be set'
    
    context = {
        tree_items_form_data: tree_items_form_data
    }
    return render(request, 'base/treeItemsCreate.html', context) 

# get systems to populate the dropdowns
def get_tree_items(request):
    request_data = json.loads(request.body.decode('utf-8'))
    selectedProjectId = request_data.get('projectId')
    selectedSystemId = request_data.get('systemId')
    selectedParentId = request_data.get('configurationId')
    
    getSystemTreeItemUrl = f'https://fracas.integralplm.com/WindchillRiskAndReliability12.0-REST/odata/Project_{selectedProjectId}/Systems({selectedSystemId})/TreeItems'

    try:
        response = requests.get(getSystemTreeItemUrl, auth=auth)
        print(response)
        if response.status_code == 200:
            allParentTreeItems = response.json()
            tree_items_data = [{'ID': treeItem['ParentID'], 'Name': treeItem['Name']} for treeItem in allParentTreeItems['value']]
            request.session['tree_items_data'] = tree_items_data[1:] #in the session we only want the items names

            return JsonResponse({'allParentTreeItems': tree_items_data})
        elif response.status_code == 400:
            return JsonResponse({'allParentTreeItems': None})
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return  HttpResponseServerError("An error occurred while fetching systems data")
    