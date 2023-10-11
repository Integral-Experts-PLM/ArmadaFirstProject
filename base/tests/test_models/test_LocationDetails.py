from django.test import TestCase
from datetime import date
from ...models import IncidentInfo, LocationDetails

class LocationDetailsTestCase(TestCase):

    def setUp(self):
        self.incident = IncidentInfo.objects.create(incident_ID="test_incident", occurrence_date=date.today())

    def test_location_details_creation(self):
        location = LocationDetails.objects.create(incident_ID=self.incident, user_text4_location="TestLocation")
        self.assertEqual(location.user_text4_location, "TestLocation")

    def test_location_details_update(self):
        location = LocationDetails.objects.create(incident_ID=self.incident, user_text4_location="TestLocation")
        location.user_text4_location = "UpdatedLocation"
        location.save()

        updated_location = LocationDetails.objects.get(id=location.id)
        self.assertEqual(updated_location.user_text4_location, "UpdatedLocation")

    def test_location_details_deletion(self):
        location = LocationDetails.objects.create(incident_ID=self.incident)
        location_id = location.id
        location.delete()

        with self.assertRaises(LocationDetails.DoesNotExist):
            LocationDetails.objects.get(id=location_id)

    def test_foreign_key_cascade_on_delete(self):
        location = LocationDetails.objects.create(incident_ID=self.incident)
        self.incident.delete()

        with self.assertRaises(LocationDetails.DoesNotExist):
            LocationDetails.objects.get(id=location.id)

    def test_null_and_blank_field_constraints(self):
        location = LocationDetails.objects.create(incident_ID=self.incident)

        self.assertIsNone(location.user_text4_location)
        self.assertIsNone(location.user_text24_address)
        self.assertIsNone(location.user_text25_contact)
        self.assertIsNone(location.user_text22_phone)
        self.assertIsNone(location.user_text21_email)

    # def test_email_field_content(self):
    #     valid_email = "test@example.com"
    #     location = LocationDetails.objects.create(incident_ID=self.incident, user_text21_email=valid_email)
    #     self.assertEqual(location.user_text21_email, valid_email)

    #     invalid_email = "testexample.com"
    #     with self.assertRaises(ValueError):  # This assumes some email validation, which Django doesn't do by default on CharField.
    #         LocationDetails.objects.create(incident_ID=self.incident, user_text21_email=invalid_email)
