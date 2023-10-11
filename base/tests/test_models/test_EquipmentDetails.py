from django.test import TestCase
from datetime import date
from ...models import IncidentInfo, EquipmentDetails


class EquipmentDetailsTestCase(TestCase):
    def setUp(self):
        # Assuming IncidentInfo model has a field named incident_ID
        self.incident = IncidentInfo.objects.create(incident_ID="test_incident", occurrence_date=date.today())

    def test_equipment_details_creation(self):
        equipment = EquipmentDetails.objects.create(incident_ID=self.incident)
        self.assertIsInstance(equipment, EquipmentDetails)

    def test_equipment_details_str_method(self):
        equipment = EquipmentDetails.objects.create(incident_ID=self.incident)
        self.assertEqual(str(equipment), "test_incident")

    def test_equipment_details_fields(self):
        equipment = EquipmentDetails.objects.create(
            incident_ID=self.incident,
            failed_component="TestComponent",
            serial_number="1234567890",
            meter_reading_tsn="100",
            time_to_failure_tso="50",
            user_text10_oem="OEM_Text",
            analysis_team="TestTeam"
        )
        
        self.assertEqual(equipment.failed_component, "TestComponent")
        self.assertEqual(equipment.serial_number, "1234567890")
        self.assertEqual(equipment.meter_reading_tsn, "100")
        self.assertEqual(equipment.time_to_failure_tso, "50")
        self.assertEqual(equipment.user_text10_oem, "OEM_Text")
        self.assertEqual(equipment.analysis_team, "TestTeam")

    def test_equipment_details_update(self):
        equipment = EquipmentDetails.objects.create(incident_ID=self.incident, failed_component="InitialComponent")
        equipment.failed_component = "UpdatedComponent"
        equipment.save()

        updated_equipment = EquipmentDetails.objects.get(id=equipment.id)
        self.assertEqual(updated_equipment.failed_component, "UpdatedComponent")

    def test_equipment_details_deletion(self):
        equipment = EquipmentDetails.objects.create(incident_ID=self.incident)
        equipment_id = equipment.id
        equipment.delete()

        with self.assertRaises(EquipmentDetails.DoesNotExist):
            EquipmentDetails.objects.get(id=equipment_id)

    def test_foreign_key_cascade_on_delete(self):
        equipment = EquipmentDetails.objects.create(incident_ID=self.incident)
        self.incident.delete()

        with self.assertRaises(EquipmentDetails.DoesNotExist):
            EquipmentDetails.objects.get(id=equipment.id)

    def test_equipment_details_update(self):
        equipment = EquipmentDetails.objects.create(incident_ID=self.incident, failed_component="InitialComponent")
        equipment.failed_component = "UpdatedComponent"
        equipment.save()

        updated_equipment = EquipmentDetails.objects.get(id=equipment.id)
        self.assertEqual(updated_equipment.failed_component, "UpdatedComponent")

    def test_equipment_details_deletion(self):
        equipment = EquipmentDetails.objects.create(incident_ID=self.incident)
        equipment_id = equipment.id
        equipment.delete()

        with self.assertRaises(EquipmentDetails.DoesNotExist):
            EquipmentDetails.objects.get(id=equipment_id)

    def test_foreign_key_cascade_on_delete(self):
        equipment = EquipmentDetails.objects.create(incident_ID=self.incident)
        self.incident.delete()

        with self.assertRaises(EquipmentDetails.DoesNotExist):
            EquipmentDetails.objects.get(id=equipment.id)

    def test_null_and_blank_field_constraints(self):
        equipment = EquipmentDetails.objects.create(incident_ID=self.incident)

        # The fields can be left blank upon creation, so they should be None (since they are CharFields with null=True)
        self.assertIsNone(equipment.failed_component)
        self.assertIsNone(equipment.serial_number)
        self.assertIsNone(equipment.meter_reading_tsn)
        self.assertIsNone(equipment.time_to_failure_tso)
        self.assertIsNone(equipment.user_text10_oem)
        self.assertIsNone(equipment.analysis_team)
