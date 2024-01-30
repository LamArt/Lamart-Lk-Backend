import unittest
from unittest.mock import patch, Mock
from rest_framework import status
from authentication.models import ProviderToken

from salary.views import SalaryView, SalaryStoryPoints, StatisticsStoryPointsView


class TestSalaryView(unittest.TestCase):

    @patch('salary.views.SalaryStoryPoints')
    @patch('salary.views.ProviderToken.objects.get')
    def test_get_salary_data_success(self, mock_provider_token, mock_story_points):
        mock_request = Mock()
        mock_story_points.return_value.get_salary_data.return_value = {
            "total_salary": 6500,
            'projects': {
                "VMS": {
                    "role": "Backend-developer",
                    'story_points': 40,
                    "rate": 650,
                    "salary": 3250,
                    "reward": 5000,
                    "credit": 2000
                },
            },
        }

        view = SalaryView()
        response = view.get(mock_request)

        expected_data = {
            "total_salary": 6500,
            'projects': {
                "VMS": {
                    "role": "Backend-developer",
                    'story_points': 40,
                    "rate": 650,
                    "salary": 3250,
                    "reward": 5000,
                    "credit": 2000
                },
            },
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    @patch('salary.views.ProviderToken.objects.get')
    def test_get_salary_data_not_connected_jira(self, mock_provider_token):
        mock_request = Mock()
        mock_provider_token.side_effect = ProviderToken.DoesNotExist()

        view = SalaryView()
        response = view.get(mock_request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Jira not connected')

    @patch('salary.views.SalaryStoryPoints')
    @patch('salary.views.ProviderToken.objects.get')
    def test_get_salary_data_unauthorized(self, mock_provider_token, mock_user_story_points):
        mock_request = Mock()
        mock_user_story_points.side_effect = KeyError()

        view = SalaryView()
        response = view.get(mock_request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, 'Unauthorized, make jira authentication again')


class TestStatisticsStoryPointsView(unittest.TestCase):

    @patch('salary.views.SalaryStoryPoints')
    @patch('salary.views.ProviderToken.objects.get')
    def test_get_salary_data_success(self, mock_provider_token, mock_story_points):
        mock_request = Mock()
        mock_story_points.return_value.count_by_months.return_value = {'December': 10, 'November': 30, 'October': 5}

        view = StatisticsStoryPointsView()
        response = view.get(mock_request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == '__main__':
    unittest.main()
