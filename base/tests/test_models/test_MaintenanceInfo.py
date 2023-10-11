from django.test import TestCase
from datetime import date
from django.utils import timezone
from ...models import IncidentInfo, MaintenanceInfo
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class MaintenanceInfoTestCase(TestCase):

    def setUp(self):
         self.incident = IncidentInfo.objects.create(incident_ID="test_incident", occurrence_date=date.today())
    
    def test_string_representation(self):
        maintenance_info = MaintenanceInfo.objects.create(incident_ID=self.incident, maintenance_start_date=timezone.now(), maintenance_log_identifier="test_log")
        self.assertEqual(str(maintenance_info), "test_incident")

    def test_max_length_violation(self):
        long_string = "A" * 201
        maintenance_info = MaintenanceInfo.objects.create(incident_ID=self.incident, maintenance_log_identifier=long_string, maintenance_start_date=timezone.now())
        # incident = IncidentInfo(**self.valid_data)
        # Creating an IncidentInfo object with an over-length incident_ID should raise a ValueError
        with self.assertRaises(ValidationError):
            maintenance_info.full_clean()

    def test_date_field_content(self):
        test_date = timezone.now()
        maintenance_info = MaintenanceInfo.objects.create(incident_ID=self.incident, maintenance_start_date=test_date, maintenance_log_identifier="test_log")
        self.assertEqual(maintenance_info.maintenance_start_date, test_date)

    def test_float_field_content(self):
        test_cost_item = 1234.56
        maintenance_info = MaintenanceInfo.objects.create(incident_ID=self.incident, maintenance_start_date=timezone.now(), maintenance_log_identifier="test_log", cost_item=test_cost_item)
        self.assertEqual(maintenance_info.cost_item, test_cost_item)

    def test_integer_field_content(self):
        test_number_of_men = 5
        maintenance_info = MaintenanceInfo.objects.create(incident_ID=self.incident, maintenance_start_date=timezone.now(), maintenance_log_identifier="test_log", number_of_men=test_number_of_men)
        self.assertEqual(maintenance_info.number_of_men, test_number_of_men)

    def test_incident_ID_cannot_be_null(self):
        with self.assertRaises(IntegrityError):
            MaintenanceInfo.objects.create(incident_ID=None, maintenance_start_date=timezone.now(), maintenance_log_identifier="test_log")

    def test_maintenance_start_date_cannot_be_null(self):
        with self.assertRaises(IntegrityError):
            MaintenanceInfo.objects.create(incident_ID=self.incident, maintenance_start_date=None, maintenance_log_identifier="test_log")

    def test_maintenance_log_identifier_cannot_be_null(self):
        with self.assertRaises(IntegrityError):
            MaintenanceInfo.objects.create(incident_ID=self.incident, maintenance_start_date=timezone.now(), maintenance_log_identifier=None)



