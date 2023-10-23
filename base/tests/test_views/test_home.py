from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from ... models import IncidentInfo
from ... views.views import home
from unittest.mock import patch

class HomeViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='blabla' , password='blabla')

    def test_home_view_with_authenticated_user(self):
        self.client.login(username=settings.API_USERNAME, password=settings.API_PASSWORD)
        url = reverse('home')
        with patch('base.views.views.get_projects') as mock_get_projects:
            mock_get_projects.return_value = [{'project_id': 1, 'name': 'Project 1'}, {'project_id': 2, 'name': 'Project 2'}]
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

# TO DO
    # def test_home_view_with_unauthenticated_user(self):
    #     url = reverse('home')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 404)
    #     # self.assertRedirects(response, reverse('login') + f'?next={url}')


    def test_home_view_with_no_projects(self):
        # Test that the view handles the case where no projects are returned.
        self.client.login(username=settings.API_USERNAME, password=settings.API_PASSWORD)
        url = reverse('home')
        with patch('base.views.views.get_projects') as mock_get_projects:
            mock_get_projects.return_value = []  # Simulate no projects being returned.
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')
        # self.assertContains(response, 'No projects available') 