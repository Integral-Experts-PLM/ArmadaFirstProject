from django.test import TestCase
from django.core.exceptions import ValidationError
from ...models import IncidentInfo, IncidentAnalysis
from datetime import date

class IncidentAnalysisTestCase(TestCase):

    def setUp(self):
        self.incident = IncidentInfo.objects.create(incident_ID="test_incident", occurrence_date=date.today())         

    def test_string_representation(self):
        incident_analysis = IncidentAnalysis.objects.create(incident_ID=self.incident, analysis_result="Sample result")
        self.assertEqual(str(incident_analysis), "test_incident")

    def test_max_length_constraints(self):
        long_string = "A" * 201
        with self.assertRaises(ValidationError):
            incident_analysis = IncidentAnalysis.objects.create(incident_ID=self.incident, user_text11_team_analysis=long_string)
            incident_analysis.full_clean()

    def test_text_field_content(self):
        result = "Sample analysis result"
        recommendation = "Sample recommendation"
        incident_analysis = IncidentAnalysis.objects.create(incident_ID=self.incident, analysis_result=result, analysis_recomendation=recommendation)
        self.assertEqual(incident_analysis.analysis_result, result)
        self.assertEqual(incident_analysis.analysis_recomendation, recommendation)

    def test_foreign_key_relationship(self):
        incident_analysis = IncidentAnalysis.objects.create(incident_ID=self.incident)
        self.assertEqual(incident_analysis.incident_ID.incident_ID, "test_incident")

    def test_nullable_fields(self):
        incident_analysis = IncidentAnalysis.objects.create(incident_ID=self.incident)
        self.assertIsNone(incident_analysis.user_text11_team_analysis)
        self.assertIsNone(incident_analysis.failure_detection)
        self.assertIsNone(incident_analysis.failure_mode)
        self.assertIsNone(incident_analysis.user_text16_part_category)
        self.assertIsNone(incident_analysis.root_cause)
        self.assertIsNone(incident_analysis.analysis_result)
        self.assertIsNone(incident_analysis.analysis_recomendation)

    def test_cascade_delete(self):
        incident_analysis = IncidentAnalysis.objects.create(incident_ID=self.incident)
        self.incident.delete()
        with self.assertRaises(IncidentAnalysis.DoesNotExist):
            IncidentAnalysis.objects.get(pk=incident_analysis.id)
