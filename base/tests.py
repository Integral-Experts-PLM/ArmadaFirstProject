from django.test import TestCase
from datetime import datetime
from .models import IncidentInfo
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class IncidentInfoModelTests(TestCase):

    def setUp(self):
        """
        Set up initial data for the tests. This method will be run before each test.
        """
        # Define a dictionary with valid data for an IncidentInfo instance
        self.valid_data = {
            'incident_id': 'INC001',
            'system_id': 'SYS001',
            'project_id': 'PROJ001',
            'incident_date': datetime.now(),
            #'current_state': 'NEW INCIDENT'
        }

    def test_incident_creation(self):
        """
        Test the basic creation of an IncidentInfo instance.
        """
        # Create an IncidentInfo object using the valid data
        incident = IncidentInfo.objects.create(**self.valid_data)
        
        # Check if the default value of current_state is 'NEW INCIDENT'
        self.assertEqual(incident.current_state, 'NEW INCIDENT')
        
        # Check if created_at is populated (i.e., not None) upon object creation
        self.assertIsNotNone(incident.created_at)

    def test_string_representation(self):
        """
        Test the string representation (__str__) of the IncidentInfo instance.
        """
        # Create an IncidentInfo object using the valid data
        incident = IncidentInfo.objects.create(**self.valid_data)
        
        # The string representation should be equal to the incident_id
        self.assertEqual(str(incident), 'INC001')

    def test_max_length_violation(self):
        """
        Test the max length constraint of the incident_id field.
        """
        # Set the incident_id to be longer than its defined max length (200 chars)
        self.valid_data['incident_id'] = 'I' * 201
        incident = IncidentInfo(**self.valid_data)
         # Creating an IncidentInfo object with an over-length incident_id should raise a ValueError
        with self.assertRaises(ValidationError):
            incident.full_clean()

    def test_datetime_fields_validity(self):
        # Valid DateTime should be accepted
        try:
            IncidentInfo.objects.create(**self.valid_data)
        except ValidationError:
            self.fail("Valid DateTime should be accepted for 'incident_date'")
        
        # Invalid DateTime should raise ValidationError
        self.valid_data['incident_date'] = "invalid_date"
        with self.assertRaises(ValidationError):
            IncidentInfo.objects.create(**self.valid_data)

    def test_fields_accept_null(self):
        # Fields that are optional should accept null values
        self.valid_data['reportedBy'] = None
        self.valid_data['configuration'] = None
        try:
            IncidentInfo.objects.create(**self.valid_data)
        except ValidationError:
            self.fail("Optional fields should accept null values")

    def test_field_updates(self):
        incident = IncidentInfo.objects.create(**self.valid_data)
        new_system_id = "SYS002"
        incident.system_id = new_system_id
        incident.save()

        # Fetch from DB again and check if update was successful
        incident_refreshed = IncidentInfo.objects.get(pk=incident.pk)
        self.assertEqual(incident_refreshed.system_id, new_system_id)

    def test_default_current_state(self):
        # If current_state is not provided, it should default to 'NEW INCIDENT'
        del self.valid_data['current_state']
        incident = IncidentInfo.objects.create(**self.valid_data)
        self.assertEqual(incident.current_state, 'NEW INCIDENT')

    # def test_incident_id_uniqueness(self):
    #     IncidentInfo.objects.create(**self.valid_data)
        
    #     # Creating another incident with same incident_id should raise an error
    #     with self.assertRaises(IntegrityError):
    #         IncidentInfo.objects.create(**self.valid_data)

    
