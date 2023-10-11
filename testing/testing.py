def updateIncident(request, pk):
    try:
        incident = get_object_or_404(IncidentInfo, pk=pk)
        equipment = get_object_or_404(EquipmentDetails, pk=pk)
        user_text4_location = get_object_or_404(LocationDetails, pk=pk)
        maintenance = get_object_or_404(MaintenanceInfo, pk=pk)
        incident_detail = get_object_or_404(IncidentDetail, pk=pk)
        incident_analysis = get_object_or_404(IncidentAnalysis, pk=pk)

    except IncidentInfo.DoesNotExist:
        return render(request, '404.html', status=404)

    if request.method == 'POST':
        # Create forms for each model and populate them with POST data
        incident_form = IncidentInfoForm(request.POST, instance=incident)
        equipment_form = EquipmentDetailsForm(request.POST, instance=equipment)
        location_form = LocationDetailsForm(request.POST, instance=user_text4_location)
        maintenance_form = MaintenanceInfoForm(
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
        location_form = LocationDetailsForm(instance=user_text4_location)
        maintenance_form = MaintenanceInfoForm(instance=maintenance)
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
