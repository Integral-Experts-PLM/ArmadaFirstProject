import pprint
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import IncidentInfo, EquipmentDetails, LocationDetails, MaintananceInfo, IncidentDetail, IncidentAnalysis
from .forms import IncidentInfoForm, EquipmentDetailsForm, LocationDetailsForm, MaintananceInfoForm, IncidentDetailForm, IncidentAnalysisForm

# Create your views here.


def home(request):
    incidents = IncidentInfo.objects.all()
    context = {'incidents': incidents}

    # incident = get_object_or_404(IncidentInfo, incident_id=incident_id)
    # context = {'incident': incident}

    return render(request, 'base/home.html', context)

def createIncident(request):
    incident_info_form = IncidentInfoForm(request.POST)

    if request.method == 'POST':
        print(incident_info_form.data)
        if incident_info_form.is_valid():
            incident_info = incident_info_form.save()
        else:
            print('from incident data', incident_info_form.errors.as_data())
            incident_info_form = IncidentInfoForm()

        # equipment_details_form = EquipmentDetailsForm(request.POST)
        # print(equipment_details_form.data)
        # if equipment_details_form.is_valid():
        #     equipment_details = equipment_details_form.save(commit=False)
        #     equipment_details.incident_id = incident_info
        #     equipment_details.save()
        # else:
        #     print('from equipment data', equipment_details_form.errors.as_data())
        # equipment_details_form = EquipmentDetailsForm()

        return redirect('home')    
       
    context = {'incident_info_form': incident_info_form, 'view': 'create_incident'
}
    return render(request, 'base/createIncident.html', context)

def incidentReviewAnalysis(request):
    # incident = get_object_or_404(IncidentInfo.objects.select_related('initial_info', 'detail_info', 'review', 'analysis'), pk=str(pk))
    # context = {'incident': incident}

    return render(request, 'base/incidentReviewAnalysis.html')


def updateIncident(request, pk):
    try:
        incident = get_object_or_404(IncidentInfo, pk=pk)
        equipment = get_object_or_404(EquipmentDetails, pk=pk)
        location = get_object_or_404(LocationDetails, pk=pk)
        maintenance = get_object_or_404(MaintananceInfo, pk=pk)
        incident_detail = get_object_or_404(IncidentDetail, pk=pk)
        incident_analysis = get_object_or_404(IncidentAnalysis, pk=pk)

    except IncidentInfo.DoesNotExist:
        return render(request, '404.html', status=404)

    if request.method == 'POST':
        # Create forms for each model and populate them with POST data
        incident_form = IncidentInfoForm(request.POST, instance=incident)
        equipment_form = EquipmentDetailsForm(request.POST, instance=equipment)
        location_form = LocationDetailsForm(request.POST, instance=location)
        maintenance_form = MaintananceInfoForm(
            request.POST, instance=maintenance)
        incident_detail_form = IncidentDetailForm(
            request.POST, instance=incident_detail)
        incident_analysis_form = IncidentAnalysisForm(
            request.POST, instance=incident_analysis)

        # Check if all forms are valid
        if all([
            incident_form.is_valid(),
            equipment_form.is_valid(),
            location_form.is_valid(),
            maintenance_form.is_valid(),
            incident_detail_form.is_valid(),
            incident_analysis_form.is_valid(),
        ]):
            # Save each form individually to update the associated model instances
            incident_form.save()
            equipment_form.save()
            location_form.save()
            maintenance_form.save()
            incident_detail_form.save()
            incident_analysis_form.save()
            return redirect('home')  # Redirect after successful update

    else:
        # Create forms for each model and populate them with instance data
        incident_form = IncidentInfoForm(instance=incident)
        equipment_form = EquipmentDetailsForm(instance=equipment)
        location_form = LocationDetailsForm(instance=location)
        maintenance_form = MaintananceInfoForm(instance=maintenance)
        incident_detail_form = IncidentDetailForm(instance=incident_detail)
        incident_analysis_form = IncidentAnalysisForm(
            instance=incident_analysis)

    context = {
        'incident_form': incident_form,
        'equipment_details': equipment_form,
        'location_details': location_form,
        'maintenance_info': maintenance_form,
        'incident_details': incident_detail_form,
        'incident_analysis': incident_analysis_form,
        'incident': incident,
    }
    return render(request, 'base/updateIncident.html', context)


def deleteIncident(request, pk):
    incident = get_object_or_404(IncidentInfo, pk=pk)

    if request.method == 'POST':
        incident.delete()
        return redirect('home')

    context = {'incident': incident, 'view': 'delete_incident', }
    return render(request, 'base/deleteIncident.html', context)


def viewIncident(request, pk):
    # Use get_object_or_404 to retrieve the IncidentInfo instance
    incident = get_object_or_404(IncidentInfo, pk=pk)

    # Access related objects with correct lowercase names
    equipment_details = incident.equipmentdetails_set.all()
    location_details = incident.locationdetails_set.all()
    maintenance_info = incident.maintananceinfo_set.all()
    incident_details = incident.incidentdetail_set.all()
    incident_analysis = incident.incidentanalysis_set.all()

    context = {
        'incident': incident,
        'equipment_details': equipment_details,
        'location_details': location_details,
        'maintenance_info': maintenance_info,
        'incident_details': incident_details,
        'incident_analysis': incident_analysis,
        'view': 'view_incident',
    }

    # Render the template and pass the context
    return render(request, 'base/viewIncident.html', context)

    # try:
    #     # Create a pretty printer
    #     pretty_printer = pprint.PrettyPrinter(indent=4)

    #     # Print the incident data
    #     print("IncidentInfo Data:")
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


def insert_new_record(request):
    # Add your logic here to insert a new record
    # For example, you can save data to the database or perform any desired action.
    # You can customize the response as needed.
    return HttpResponse("New record inserted successfully")


createIncident
