from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createIncident/', views.createIncident, name='createIncident'),
    path('updateIncident/', views.updateIncident, name='updateIncident'),
    # dynamic value - check if pk is interger or string from the source
    path('viewIncident/<str:pk>', views.viewIncident, name='viewIncident')
]