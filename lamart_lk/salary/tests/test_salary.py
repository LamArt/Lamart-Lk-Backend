import unittest
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime, timedelta

from salary.utils.salary import SalaryStoryPoints
from salary.utils.profile import AtlassianUserProfile


class TestSalaryStoryPoints(unittest.TestCase):

    @patch('salary.utils.profile.AtlassianProvider')
    def setUp(self, mock_atlassian_provider):
        self.story_points = SalaryStoryPoints('refresh_token', 1)
        self.project = 'TEST'

    @patch('salary.utils.profile.AtlassianUserProfile.take_tasks')
    def test_count_story_points_by_projects(self, mock_take_tasks):
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

        result = self.story_points.count_story_points_by_projects(self.project, 'startOfMonth()', email=None)

        mock_take_tasks.assert_called_once_with('TEST', 'startOfMonth()', None)
        self.assertEqual(result, {self.project: 16})

    @patch('salary.utils.salary.AtlassianUserProfile.take_tasks')
    def test_count_story_points_by_projects_none_issue_data(self, mock_take_tasks):
        mock_take_tasks.return_value = None
        result = self.story_points.count_story_points_by_projects(self.project, 'startOfMonth()', email=None)
        self.assertEqual(result, {})

    # Rewrite tests with new functionality!
    # @patch('salary.utils.salary.SalaryStoryPoints.count_story_points_by_projects')
    # @patch('salary.utils.projects.EmployeeProjectManager.calculate_salary')
    # def test_count_salary_for_team_leader_by_project(self, mock_calculate_salary, mock_count_story_points):
    #     project = {'jira_key': 'TEST', 'rate': 650}
    #     period = 'startOfMonth()'
    #
    #     mock_count_story_points.return_value = {'TEST': 3}
    #     mock_calculate_salary.return_value = 365
    #
    #     result = self.story_points.count_salary_for_team_leader_by_project(project, period)
    #     expected_result = {'story_points': 9, 'salary': 1095}
    #
    #     self.assertEqual(result, expected_result)
    #
    # @patch('salary.utils.salary.AtlassianUserProfile.take_tasks')
    # def test_count_by_months_success(self, mock_take_tasks):
    #     self.story_points.current_date = datetime(2023, 12, 12)
    #
    #     mock_take_tasks.return_value = {
    #         'issues': [
    #             {
    #                 'fields': {'customfield_10016': 3, 'created': '2023-10-15T12:00:00.000+0000'}
    #             },
    #             {
    #                 'fields': {'customfield_10016': 5, 'created': '2023-11-05T12:00:00.000+0000'}
    #             },
    #             {
    #                 'fields': {'customfield_10016': 2, 'created': '2023-12-01T12:00:00.000+0000'}
    #             },
    #             {
    #                 'fields': {'customfield_10016': 1, 'created': '2023-10-25T12:00:00.000+0000'}
    #             },
    #             {
    #                 'fields': {'customfield_10016': 8, 'created': '2023-11-15T12:00:00.000+0000'}
    #             },
    #             {
    #                 'fields': {'customfield_10016': 6, 'created': '2023-12-01T12:00:00.000+0000'}
    #             },
    #         ]
    #     }
    #
    #     result = self.story_points.count_by_months()
    #
    #     expected_result = {'December': 8, 'November': 13, 'October': 4}
    #     self.assertEqual(result, expected_result)
    #
    #     mock_take_tasks.assert_called_once_with('startOfMonth(-12M)')
    #
    # @patch('salary.utils.story_points.AtlassianUserProfile.take_tasks')
    # def test_count_by_months_none_issue_data(self, mock_take_tasks):
    #     mock_take_tasks.return_value = None
    #     result = self.story_points.count_by_months()
    #     self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
