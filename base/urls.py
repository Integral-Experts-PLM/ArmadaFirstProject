from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home-create-incident/', views.homeCreateIncident, name='home_create_incident'),
    path('create-incident/<str:project_id>/<str:system_id>/', views.createIncident, name='create_incident'),
    path('view-incident/<str:project_id>/<str:system_id>/<str:incident_ID>/', views.viewIncident, name='view_incident'),
    path('update-incident/<str:project_id>/<str:system_id>/<str:incident_ID>/', views.updateIncident, name='update_incident'),
    path('delete-incident/<str:pk>/', views.deleteIncident, name='delete_incident'),

    # subTabs
    path('maintenance-logs/', views.viewMaintenanceLogs, name='maintenance_logs'),
    path('operating-times/', views.viewOperatingTimes, name='operating_times'),
    path('incident-report/', views.viewIncidentReport, name='incident_report'),
    path('analysis/', views.viewAnalysis, name='analysis'),
    path('review-board/', views.viewReviewBoard, name='review_board'),
    path('overview/', views.viewOverview, name='overview'),

    # popup
    path('maintenance-log-create/', views.maintenanceLogCreate, name='maintenance_log_create'),


    path('insert-new-record/', views.insert_new_record, name='insert_new_record'),
    # in the future, this page will need a pk
    path('incident-review-analysis/', views.incidentReviewAnalysis, name='incident_review_analysis'),
]