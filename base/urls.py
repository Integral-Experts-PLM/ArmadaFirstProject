from django.urls import path
from . import views

urlpatterns = [
    # main crud
    path('', views.home, name='home'),
    path('create-incident/', views.createIncident, name='create_incident'),
    path('update-incident/<str:project_id>/<str:system_id>/<str:incident_ID>/', views.updateIncident, name='update_incident'),
    path('delete-incident/<str:pk>/', views.deleteIncident, name='delete_incident'),

    # subTabs
    path('view-all-incidents/', views.viewAllIncidents, name='view_all_incidents'),
    path('maintenance-logs/', views.viewMaintenanceLogs, name='maintenance_logs'),
    path('operating-times/', views.viewOperatingTimes, name='operating_times'),
    path('incident-report/', views.viewIncidentReport, name='incident_report'),
    path('analysis/', views.viewAnalysis, name='analysis'),
    path('review-board/', views.viewReviewBoard, name='review_board'),
    path('overview/', views.viewOverview, name='overview'),

    # popup
    path('maintenance-log-create/', views.maintenanceLogCreate, name='maintenance_log_create'),

    # only get data, no page render
    path('get-systems/', views.get_systems, name='get_systems'),



    path('insert-new-record/', views.insert_new_record, name='insert_new_record'),
    # in the future, this page will need a pk
    path('incident-review-analysis/', views.incidentReviewAnalysis, name='incident_review_analysis'),
]