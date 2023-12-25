import unittest
from unittest.mock import patch, Mock

from rest_framework.response import Response
from rest_framework import status

from salary.utils.profile import AtlassianUserProfile


class TestAtlassianUserProfile(unittest.TestCase):

    @patch('salary.utils.profile.AtlassianProvider')
    def setUp(self, mock_atlassian_provider):
        self.atlassian_profile = AtlassianUserProfile(refresh='fake_token', user=1)

    def test_get_cloud_id(self):
        mock_response = Mock()
        mock_response.json.return_value = [{'id': 'fake_cloud_id'}]
        mock_response.status_code = 200

        with patch('salary.utils.profile.requests.get', return_value=mock_response) as mock_get:
            cloud_id = self.atlassian_profile.get_cloud_id()
            mock_get.assert_called_once_with(self.atlassian_profile.ACCESSIBLE_RESOURCES,
                                             headers=self.atlassian_profile.headers)

        self.assertEqual(cloud_id, 'fake_cloud_id')

    def test_get_email(self):
        mock_response = Mock()
        mock_response.json.return_value = {'emailAddress': 'fake@ya.ru'}
        mock_response.status_code = 200

        with patch('salary.utils.profile.requests.get', return_value=mock_response) as mock_get:
            email = self.atlassian_profile.get_email()
            mock_get.assert_called_once_with(f'{self.atlassian_profile.search_url}/myself',
                                             headers=self.atlassian_profile.headers)

        self.assertEqual(email, 'fake@ya.ru')

    @patch('salary.utils.profile.AtlassianUserProfile.get_email', return_value='fake@ya.ru')
    def test_created_tasks(self, mock_get_email):
        projects = ['TEST-1', 'TEST-2', 'TEST-3']
        email = self.atlassian_profile.get_email()

        mock_response = Mock()
        mock_response.json.return_value = {
            'issues': [
                {
                    'id': '10035',
                    'key': 'TEST-3',
                    'fields': {'customfield_10016': 1.0, 'created': '2023-12-12'}
                }
            ]
        }
        mock_response.status_code = 200

        with patch('salary.utils.profile.requests.get', return_value=mock_response) as mock_get:
            tasks = self.atlassian_profile.take_tasks(projects, created_type='2023-12-12')
            jql_query = f'(project=TEST-1 OR project=TEST-2 OR project=TEST-3) AND created>=2023-12-12 AND assignee="{email}" AND status IN ("DONE", "НА ПРОВЕРКЕ")'

            mock_get.assert_called_once_with(
                f'{self.atlassian_profile.search_url}/search',
                headers=self.atlassian_profile.headers,
                params={'jql': jql_query, 'fields': 'customfield_10016,created', 'maxResults': 100000}
            )

        self.assertEqual(tasks, {'issues': [
            {'id': '10035', 'key': 'TEST-3',
             'fields': {'customfield_10016': 1.0, 'created': '2023-12-12'}
             }]
        })


if __name__ == '__main__':
    unittest.main()
