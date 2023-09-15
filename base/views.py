import pprint
from django.shortcuts import render, get_object_or_404
from .models import Incident, IncidentInitialInfo, IncidentDetailInfo, IncidentReview, IncidentAnalysis

# Create your views here.
def home(request):
    incidents = Incident.objects.all()
    context = {'incidents': incidents}
    return render(request, 'base/home.html', context)

def createIncident(request):
    # context = 'create incident'
    return render(request, 'base/createIncident.html')

def updateIncident(request):
    # context = 'update incident'
    return render(request, 'base/updateIncident.html')

def viewIncident(request, pk):
    incident = get_object_or_404(Incident.objects.select_related('initial_info', 'detail_info', 'review', 'analysis'), pk=str(pk))

    context = {'incident': incident}

    # try:
    #     # Create a pretty printer
    #     pretty_printer = pprint.PrettyPrinter(indent=4)

    #     # Print the incident data
    #     print("Incident Data:")
    #     pretty_printer.pprint(incident.__dict__)

    #     # Print related data in a friendly format
    #     if incident.initial_info:
    #         print("Related IncidentInitialInfo Data:")
    #         pretty_printer.pprint(incident.initial_info.__dict__)

    #     if incident.detail_info:
    #         print("Related IncidentDetailInfo Data:")
    #         pretty_printer.pprint(incident.detail_info.__dict__)

    #     if incident.review:
    #         print("Related IncidentReview Data:")
    #         pretty_printer.pprint(incident.review.__dict__)

    #     if incident.analysis:
    #         print("Related IncidentAnalysis Data:")
    #         pretty_printer.pprint(incident.analysis.__dict__)

    # except AttributeError as e:
    #     print(f"An error occurred: {e}")

    return render(request, 'base/viewIncident.html', context)