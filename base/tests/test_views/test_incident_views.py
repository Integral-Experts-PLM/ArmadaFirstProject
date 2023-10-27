from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

class YourAppViewsTestCase(TestCase):

    @patch('base.home_views.requests.get')
    def test_viewAllIncidents(self, mock_get):
        # Mock the response from the external API
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'value': [{'incident_id': 1}, {'incident_id': 2}]
        }

        # Set session variables if needed
        self.client.session['project_id'] = 'your_project_id'
        self.client.session['system_id'] = 'your_system_id'

        # Access the view
        url = reverse('view-all-incidents')  # Make sure to set the correct URL name
        response = self.client.get(url)

        # Check if the view returns the expected status code
        self.assertEqual(response.status_code, 200)

        # Check if the context contains the expected data
        self.assertEqual(len(response.context['incidents_data']), 2)
        self.assertEqual(response.context['page'], 'view-all-incidents')
