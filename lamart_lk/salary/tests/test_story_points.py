import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

from salary.utils.story_points import StoryPoints
from salary.utils.profile import AtlassianUserProfile


class TestStoryPoints(unittest.TestCase):

    @patch('salary.utils.profile.AtlassianProvider')
    def setUp(self, mock_atlassian_provider):
        self.story_points = StoryPoints(refresh='fake_token', user=1)

    @patch('salary.utils.story_points.AtlassianUserProfile.take_tasks')
    def test_count_at_moment_success(self, mock_take_tasks):
        mock_take_tasks.return_value = {
            'issues': [
                {
                    'id': '1',
                    'key': 'TEST-1',
                    'fields': {'customfield_10016': 5}
                },
                {
                    'id': '2',
                    'key': 'TEST-2',
                    'fields': {'customfield_10016': 9}
                },
                {
                    'id': '3',
                    'key': 'TEST-3',
                    'fields': {'customfield_10016': 2}
                },
            ]
        }

        result = self.story_points.count_at_moment()

        mock_take_tasks.assert_called_once_with('startOfMonth()', 'sprint in openSprints() AND')
        self.assertEqual(result, 16)

    @patch('salary.utils.story_points.AtlassianUserProfile.take_tasks')
    def test_count_at_moment_none_issue_data(self, mock_take_tasks):
        mock_take_tasks.return_value = None
        result = self.story_points.count_at_moment()
        self.assertEqual(result, 0)

    @patch('salary.utils.story_points.AtlassianUserProfile.take_tasks')
    def test_count_by_months_success(self, mock_take_tasks):
        self.story_points.current_date = datetime(2023, 12, 12)

        mock_take_tasks.return_value = {
            'issues': [
                {
                    'fields': {'customfield_10016': 3, 'created': '2023-10-15T12:00:00.000+0000'}
                },
                {
                    'fields': {'customfield_10016': 5, 'created': '2023-11-05T12:00:00.000+0000'}
                },
                {
                    'fields': {'customfield_10016': 2, 'created': '2023-12-01T12:00:00.000+0000'}
                },
                {
                    'fields': {'customfield_10016': 1, 'created': '2023-10-25T12:00:00.000+0000'}
                },
                {
                    'fields': {'customfield_10016': 8, 'created': '2023-11-15T12:00:00.000+0000'}
                },
                {
                    'fields': {'customfield_10016': 6, 'created': '2023-12-01T12:00:00.000+0000'}
                },
            ]
        }

        result = self.story_points.count_by_months()

        expected_result = {'December': 8, 'November': 13, 'October': 4}
        self.assertEqual(result, expected_result)

        mock_take_tasks.assert_called_once_with('startOfMonth(-12M)')

    @patch('salary.utils.story_points.AtlassianUserProfile.take_tasks')
    def test_count_by_months_none_issue_data(self, mock_take_tasks):
        mock_take_tasks.return_value = None
        result = self.story_points.count_by_months()
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
