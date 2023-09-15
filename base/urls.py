from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-incident/', views.createIncident, name='createIncident'),
    path('update-incident/<str:pk>', views.updateIncident, name='updateIncident'),
    path('delete-incident/<str:pk>', views.deleteIncident, name='deleteIncident'),

    # in the future, this page will need a pk
    path('incident-review-analysis/', views.incidentReviewAnalysis, name='incidentReviewAnalysis'),
    path('view-incident/<str:pk>', views.viewIncident, name='viewIncident')
]