from django.db import connections
from .db_models import Incident, TreeItem
import time

# Obtener datos de TreeItem aprovechando la clave foránea de la tabla Incidents1
def get_all_incidents(set_id, configuration_id=None, tree_id=None):
    try:
         # Obtener datos de TreeItem aprovechando la clave foránea de la tabla
        queryset = Incident.objects.using('sqlserver_db').order_by('ID').select_related('TreeID')
        queryset = queryset.filter(SetID=set_id)
        
        configuration_id = None if configuration_id == '' else configuration_id # Convertir a None si es una cadena vacía
        if configuration_id is not None:
            queryset = queryset.filter(ConfigurationID=configuration_id)
        
        tree_id = None if tree_id == '' else tree_id # Convertir a None si es una cadena vacía
        if tree_id is not None:
            queryset = queryset.filter(TreeID=tree_id)

        return queryset
    except Exception as e:
        print(f"An error occurred while accessing the database: {e}")
        return None
    
def get_tree_name (tree_id):
    try:
        queryset = TreeItem.objects.using('sqlserver_db').filter(ID=tree_id).values_list('Name', flat=True)
        name = queryset.first()
        return name
    except Exception as e:
        print(f"An error occurred while accessing the database: {e}")
        return None
    


## ================================================================================== ##
## ================================================================================== ##

    ### PRUEBA PARA MOSTRAR LA DIFERENCIA EN TIEMPO DE EJECUCION SIN CLAVE FORANEA ###

# Obtener datos de TreeItem sin aprovechar la clave foránea de la tabla Incidents1
def get_all_incidents_NotOptimized(set_id, configuration_id=None, tree_id=None):
    try:
        queryset = Incident.objects.using('sqlserver_db').order_by('ID')
        queryset = queryset.filter(SetID=set_id)
        
        configuration_id = None if configuration_id == '' else configuration_id # Convertir a None si es una cadena vacía
        if configuration_id is not None:
            queryset = queryset.filter(ConfigurationID=configuration_id)
        
        tree_id = None if tree_id == '' else tree_id # Convertir a None si es una cadena vacía
        if tree_id is not None:
            queryset = queryset.filter(TreeID=tree_id)

        return queryset
    except Exception as e:
        print(f"An error occurred while accessing the database: {e}")
        return None
    
# Obtener el Name del TreeItem mediante el campo TreeID de la Incidencia
def get_tree_name (tree_id):
    try:
        queryset = TreeItem.objects.using('sqlserver_db').filter(ID=tree_id).values_list('Name', flat=True)
        name = queryset.first()
        return name
    except Exception as e:
        print(f"An error occurred while accessing the database: {e}")
        return None

## ================================================================================== ##
## ================================================================================== ##
