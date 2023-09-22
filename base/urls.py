from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-incident/', views.createIncident, name='create_incident'),
    path('view-incident/<str:pk>', views.viewIncident, name='view_incident'),
    path('update-incident/<str:pk>', views.updateIncident, name='update_incident'),
    path('delete-incident/<str:pk>', views.deleteIncident, name='delete_incident'),

    path('insert-new-record/', views.insert_new_record, name='insert_new_record'),


    # in the future, this page will need a pk
    path('incident-review-analysis/', views.incidentReviewAnalysis, name='incident_review_analysis'),
]