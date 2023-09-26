import pprint
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import IncidentInfo, EquipmentDetails, LocationDetails, MaintananceInfo, IncidentDetail, IncidentAnalysis
from .forms import IncidentInfoForm, EquipmentDetailsForm, LocationDetailsForm, MaintananceInfoForm, IncidentDetailForm, IncidentAnalysisForm, IncidentInfoIdForm


def home(request):
    message = None  # Initialize the message variable
    if request.method == 'POST':
        # Create a form to input the incident number
        incident_id_form = IncidentInfoIdForm(request.POST)
        if incident_id_form.is_valid():
            incident_id = incident_id_form.cleaned_data['incident_id']
            # Try to retrieve the incident
            try:
                incident = IncidentInfo.objects.get(incident_id=incident_id)
            except IncidentInfo.DoesNotExist:
                message = 'Invalid Incident Id!'
            else:
                return redirect('view_incident', pk=incident.pk)
    else:
        incident_id_form = IncidentInfoIdForm()

    context = {'incident_id_form': incident_id_form, 'message': message}
    return render(request, 'base/home.html', context)


def createIncident(request):
    # Create forms for the incident creation
    incident_info_form = IncidentInfoForm(request.POST or None)
    equipment_details_form = EquipmentDetailsForm(request.POST or None)
    location_details_form = LocationDetailsForm(request.POST or None)
    incident_details_form = IncidentDetailForm(request.POST or None)

    if request.method == 'POST':
        if all([incident_info_form.is_valid(), equipment_details_form.is_valid(), location_details_form.is_valid(), incident_details_form.is_valid()]):

            incident_data = incident_info_form.save(commit=False)
            incident_data.save()

            equipment_data = equipment_details_form.save(commit=False)
            equipment_data.incident_id = incident_data
            equipment_data.save()

            location_details = location_details_form.save(commit=False)
            location_details.incident_id = incident_data
            location_details.save()

            incident_details = incident_details_form.save(commit=False)
            incident_details.incident_id = incident_data
            incident_details.save()

            return redirect('home')
        else:
            incident_info_form = IncidentInfoForm()
            equipment_details_form = EquipmentDetailsForm()
            location_details_form = LocationDetailsForm()
            incident_details_form = IncidentDetailForm()

    context = {'incident_info_form': incident_info_form, 'equipment_details_form': equipment_details_form, 'location_details_form': location_details_form, 'incident_details_form': incident_details_form, 'view': 'create_incident'
               }

    return render(request, 'base/createIncident.html', context)


def incidentReviewAnalysis(request):
    # UNDER CONSTRUCTION
    # incident = get_object_or_404(IncidentInfo.objects.select_related('initial_info', 'detail_info', 'review', 'analysis'), pk=str(pk))
    # context = {'incident': incident}

    return render(request, 'base/incidentReviewAnalysis.html')


def updateIncident(request, pk):
    # Use get_object_or_404 to retrieve the IncidentInfo instance
    incident = get_object_or_404(IncidentInfo, pk=pk)

    # Access related objects
    equipment_details = EquipmentDetails.objects.filter(
        incident_id=incident).first()
    location_details = LocationDetails.objects.filter(
        incident_id=incident).first()
    incident_details = IncidentDetail.objects.filter(
        incident_id=incident).first()

    if request.method == 'POST':
        # Create forms instances to be updated
        incident_info_form = IncidentInfoForm(request.POST, instance=incident)
        equipment_details_form = EquipmentDetailsForm(
            request.POST, instance=equipment_details)
        location_details_form = LocationDetailsForm(
            request.POST, instance=location_details)
        incident_details_form = IncidentDetailForm(
            request.POST, instance=incident_details)

        if all([incident_info_form.is_valid(), equipment_details_form.is_valid(), location_details_form.is_valid(), incident_details_form.is_valid()]):
            # Save the updated data
            incident_info_form.save()
            equipment_details_form.save()
            location_details_form.save()
            incident_details_form.save()

            return redirect('home')

    else:
        # Initialize forms with existing data
        incident_info_form = IncidentInfoForm(instance=incident)
        equipment_details_form = EquipmentDetailsForm(
            instance=equipment_details)
        location_details_form = LocationDetailsForm(instance=location_details)
        incident_details_form = IncidentDetailForm(instance=incident_details)

    context = {
        'incident': incident,
        'equipment_details': equipment_details,
        'location_details': location_details,
        'incident_details': incident_details,
        'view': 'update_incident',
    }
    return render(request, 'base/updateIncident.html', context)


def deleteIncident(request, pk):
    # Use get_object_or_404 to retrieve the IncidentInfo instance
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
    equipment_details = EquipmentDetails.objects.filter(
        incident_id=incident).first()
    location_details = LocationDetails.objects.filter(
        incident_id=incident).first()
    maintenance_info = MaintananceInfo.objects.filter(
        incident_id=incident).first()
    incident_details = IncidentDetail.objects.filter(
        incident_id=incident).first()
    incident_analysis = IncidentAnalysis.objects.filter(
        incident_id=incident).first()

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


def insert_new_record(request):
    # Add your logic here to insert a new record for the  MAINTENANCE
    # UNDER CONSTRUCTION
    # For example, you can save data to the database or perform any desired action.
    # You can customize the response as needed.
    return HttpResponse("New record inserted successfully")

    #     # Create a pretty printer
    #     pretty_printer = pprint.PrettyPrinter(indent=4)

    #     # Print the incident data
    #     print("IncidentInfo Data:")
    #     pretty_printer.pprint(incident.__dict__)
