from django.test import TestCase
from datetime import datetime
from ...models import IncidentInfo
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class IncidentInfoModelTestCase(TestCase):

    def setUp(self):
        # Define a dictionary with valid data for an IncidentInfo instance
        self.valid_data = {
            'incident_ID': 'INC001',
            'system_id': 'SYS001',
            'project_id': 'PROJ001',
            'occurrence_date': datetime.now()
            # 'workflow_state': 'NEW INCIDENT'
        }

    def test_incident_creation(self):
        # Create an IncidentInfo object using the valid data
        incident = IncidentInfo.objects.create(**self.valid_data)

        # Check if the default value of workflow_state is 'NEW INCIDENT'
        self.assertEqual(incident.workflow_state, 'NEW INCIDENT')

        # Check if created_at is populated (i.e., not None) upon object creation
        self.assertIsNotNone(incident.created_at)

    def test_default_workflow_state(self):
        # If workflow_state is not provided, it should default to 'NEW INCIDENT'
        self.valid_data.pop('workflow_state', None)
        incident = IncidentInfo.objects.create(**self.valid_data)
        self.assertEqual(incident.workflow_state, 'NEW INCIDENT')

    def test_max_length_violation(self):
        # Set the incident_ID to be longer than its defined max length (200 chars)
        self.valid_data['incident_ID'] = 'I' * 201
        incident = IncidentInfo(**self.valid_data)
        with self.assertRaises(ValidationError):
            incident.full_clean()

    def test_datetime_fields_validity(self):
        # Valid DateTime should be accepted
        try:
            IncidentInfo.objects.create(**self.valid_data)
        except ValidationError:
            self.fail("Valid DateTime should be accepted for 'occurrence_date'")

        # Invalid DateTime should raise ValidationError
        self.valid_data['occurrence_date'] = "invalid_date"
        with self.assertRaises(ValidationError):
            IncidentInfo.objects.create(**self.valid_data)

    def test_fields_accept_null_and_blank(self):
        # Fields that are optional should accept null values and blank strings
        self.valid_data.update({
            'person_incident_entry': None,
            'configuration': None,
            'user_text13_tail_number': "",
            'user_text17_mission_effect': None,
        })

        try:
            IncidentInfo.objects.create(**self.valid_data)
        except ValidationError:
            self.fail("Optional fields should accept null values and blank strings")

    def test_field_updates(self):
        incident = IncidentInfo.objects.create(**self.valid_data)
        new_system_id = "SYS002"
        incident.system_id = new_system_id
        incident.save()

        # Fetch from DB again and check if update was successful
        incident_refreshed = IncidentInfo.objects.get(pk=incident.pk)
        self.assertEqual(incident_refreshed.system_id, new_system_id)

    def test_incident_ID_uniqueness(self):
        IncidentInfo.objects.create(**self.valid_data)

        # Creating another incident with the same incident_ID should raise an IntegrityError
        with self.assertRaises(Exception) as context:
            IncidentInfo.objects.create(**self.valid_data)
        self.assertTrue('unique constraint' in str(context.exception).lower())