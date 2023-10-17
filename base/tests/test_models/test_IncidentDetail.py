from django.test import TestCase
from datetime import date
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from ...models import IncidentInfo, MaintenanceInfo, IncidentDetail
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class IncidentDetailTestCase(TestCase):

    def setUp(self):
        self.incident = IncidentInfo.objects.create(incident_ID="test_incident", occurrence_date=date.today())
        self.maintenance = MaintenanceInfo.objects.create(incident_ID=self.incident, maintenance_start_date=timezone.now(), maintenance_log_identifier="test_log")

    def test_max_length_constraints(self):
        long_string = "A" * 201
        with self.assertRaises(ValidationError):
            incident_detail = IncidentDetail.objects.create(incident_ID=self.incident, operating_mode=long_string)
            incident_detail.full_clean()

    def test_text_field_content(self):
        description = "Sample incident description"
        incident_detail = IncidentDetail.objects.create(incident_ID=self.incident, description_incident=description)
        self.assertEqual(incident_detail.description_incident, description)

    def test_foreign_key_relationship(self):
        incident_detail = IncidentDetail.objects.create(incident_ID=self.incident, maintenance=self.maintenance)
        self.assertEqual(incident_detail.incident_ID.incident_ID, "test_incident")
        self.assertEqual(incident_detail.maintenance.maintenance_log_identifier, "test_log")

    def test_cascade_delete_incident(self):
        incident_detail = IncidentDetail.objects.create(incident_ID=self.incident)
        self.incident.delete()
        self.assertFalse(IncidentDetail.objects.filter(pk=incident_detail.pk).exists())

    def test_cascade_delete_maintenance(self):
        incident_detail = IncidentDetail.objects.create(incident_ID=self.incident, maintenance=self.maintenance)
        self.maintenance.delete()
        self.assertFalse(IncidentDetail.objects.filter(pk=incident_detail.pk).exists())

    def test_nullable_fields(self):
        incident_detail = IncidentDetail.objects.create(incident_ID=self.incident)
        self.assertIsNone(incident_detail.operating_mode)
        self.assertIsNone(incident_detail.user_text2_initial_severity)
        self.assertIsNone(incident_detail.description_incident)
        self.assertIsNone(incident_detail.maintenance)
        self.assertFalse(incident_detail.attachments_incidents.name)  # Check that there's no file associated
