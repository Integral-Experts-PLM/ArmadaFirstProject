from django.urls import path

from .views.tree_items_views import tree_items_views, tree_items_create

from .views.operating_times_views import operatingTimes_views, operatingTimes_create
from .views import home_views, system_views, configuration_views, maintenanceLogs_views
from .views.incident_views import read_incident_views, create_incident_views, update_incident_views, delete_incident_views

urlpatterns = [
    # main crud
    path('', home_views.home, name='home'),
    # path('create-incident-form/', create_incident_views.createIncidentForms, name='create_incident_form'),
    path('create-incident/', create_incident_views.createIncident, name='create_incident'),
    path('update-incident/<str:project_id>/<str:system_id>/<str:incident_ID>/', update_incident_views.updateIncident, name='update_incident'),
    path('delete-incident/<str:pk>/', delete_incident_views.deleteIncident, name='delete_incident'),

    # subTabs
    path('view-all-incidents/', read_incident_views.viewAllIncidents, name='view_all_incidents'),
    path('get-incident-data/', read_incident_views.getIncidentData, name='get-incident-data'),
    path('maintenance-logs/', maintenanceLogs_views.viewMaintenanceLogs, name='maintenance_logs'),
    path('operating-times/', operatingTimes_views.viewOperatingTimes, name='operating_times'),
    path('incident-report/', read_incident_views.viewIncidentReport, name='incident_report'),
    path('analysis/', read_incident_views.viewAnalysis, name='analysis'),
    path('review-board/', read_incident_views.viewReviewBoard, name='review_board'),
    path('overview/', read_incident_views.viewOverview, name='overview'),

    # creation
    path('maintenance-log-create/', home_views.maintenanceLogCreate, name='maintenance_log_create'),
    path('operating-times-create/', operatingTimes_create.operatingTimesCreate, name='operating_times_create'),
    path('tree-items-create/', tree_items_create.treeItemsCreate, name='tree_items_create'),

    # auxiliary path, only get data, no page render
    path('get-systems/', system_views.get_systems, name='get_systems'),
    path('get-configurations/', configuration_views.get_configurations, name='get_configurations'),
    path('get-tree-items/', tree_items_views.get_tree_items, name='get_tree_items'),
    path('get-tree-items-to-create/', tree_items_create.get_tree_items, name='get_tree_items_to_create'),





    # path('insert-new-record/', views.insert_new_record, name='insert_new_record'),
    # # in the future, this page will need a pk
    # path('incident-review-analysis/', views.incidentReviewAnalysis, name='incident_review_analysis'),
]