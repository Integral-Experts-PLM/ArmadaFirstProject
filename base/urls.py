from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createIncidence/', views.createIncidence, name='createIncidence'),
    path('updateIncidence/', views.updateIncidence, name='updateIncidence'),
    # dynamic value - check if pk is interger or string from the source
    path('viewIncidence/<int:pk>', views.viewIncidence, name='viewIncidence')
]