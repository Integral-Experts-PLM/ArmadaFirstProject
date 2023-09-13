from django.shortcuts import render

incidences = [
    { 'id': 1, 'incidence': 'incidentce one testing'},
    { 'id': 2, 'incidence': 'incidentce two testing'},
    { 'id': 3, 'incidence': 'incidentce tree testing'},

]
# Create your views here.
def home(request):
    context = {'incidences': incidences}
    return render(request, 'base/home.html', context)

def createIncidence(request):
    # context = 'create incidence'
    return render(request, 'base/createIncidence.html')

def updateIncidence(request):
    # context = 'update incidence'
    return render(request, 'base/updateIncidence.html')

def viewIncidence(request, pk):
    incidence = None
    for i in incidences:
        if i['id'] == int(pk):
            incidence = i
    context = {'incidence': incidence}
    # context = 'view incidence'
    return render(request, 'base/viewIncidence.html', context)
