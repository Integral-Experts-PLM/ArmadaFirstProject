from django.urls import path
from .views import views, system_views, incident_views, maintenanceLogs_views, operatingTimes_views

urlpatterns = [
    # main crud
    path('', views.home, name='home'),
    path('create-incident/', views.createIncident, name='create_incident'),
    path('update-incident/<str:project_id>/<str:system_id>/<str:incident_ID>/', views.updateIncident, name='update_incident'),
    path('delete-incident/<str:pk>/', views.deleteIncident, name='delete_incident'),

    # subTabs
    path('view-all-incidents/', incident_views.viewAllIncidents, name='view_all_incidents'),
    path('maintenance-logs/', maintenanceLogs_views.viewMaintenanceLogs, name='maintenance_logs'),
    path('operating-times/', operatingTimes_views.viewOperatingTimes, name='operating_times'),
    path('incident-report/', incident_views.viewIncidentReport, name='incident_report'),
    path('analysis/', incident_views.viewAnalysis, name='analysis'),
    path('review-board/', incident_views.viewReviewBoard, name='review_board'),
    path('overview/', incident_views.viewOverview, name='overview'),

    # maintenance
    path('maintenance-log-create/', views.maintenanceLogCreate, name='maintenance_log_create'),

    # auxiliary path, only get data, no page render
    path('get-systems/', system_views.get_systems, name='get_systems'),



    # path('insert-new-record/', views.insert_new_record, name='insert_new_record'),
    # # in the future, this page will need a pk
    # path('incident-review-analysis/', views.incidentReviewAnalysis, name='incident_review_analysis'),
]