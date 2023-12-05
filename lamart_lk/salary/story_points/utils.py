from collections import defaultdict
import requests
from datetime import datetime, timedelta

from authentication.providers.atlassian import AtlassianApiProvider


class StoryPoints(AtlassianApiProvider):
    current_date = datetime.now()

    def take_tasks(self, created_type, sprints=''):
        """Make request to jira api with JQL, return data of projects"""

        if not self.projects:
            return None
        query_of_projects = ' OR '.join([f'project={project}' for project in self.projects])
        email = self.get_user_email()
        jql_query = f'{sprints}({query_of_projects}) AND created>={created_type} AND assignee="{email}" AND status IN ("DONE", "НА ПРОВЕРКЕ")'
        params = {
            'jql': jql_query,
            'fields': 'customfield_10016,created',
            'maxResults': 100000,
        }
        rq = requests.get(f'{self.search_url}/search', headers=self.headers, params=params)
        if rq.status_code == 200:
            response_data = rq.json()
            return response_data

    def count_story_points_at_moment(self):
        """Counter sp of ALL projects with open sprints for current month"""

        issue_data = self.take_tasks('startOfMonth()', 'sprint in openSprints() AND')
        if issue_data is None:
            return 0
        total = 0
        for issue in issue_data.get('issues', []):
            story_points = issue['fields'].get('customfield_10016')
            if story_points is not None:
                total += story_points

        return total

    def count_story_points_by_months(self):
        """Counter sp for the last 10 months"""

        time_delta = 10 * 4
        issue_data = self.take_tasks('startOfMonth(-10M)')
        time_data = defaultdict(int)
        if issue_data is None:
            return {}
        for issue in issue_data.get('issues', []):
            issue_date = datetime.strptime(issue['fields']['created'][:-6], "%Y-%m-%dT%H:%M:%S.%f")

            for i in range(time_delta):
                start_time = self.current_date.replace(day=1) - timedelta(weeks=i * 4)
                end_time = (start_time.replace(day=1) +
                            timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0) - timedelta(seconds=1)

                if start_time <= issue_date <= end_time:
                    time_name = start_time.strftime('%B')
                    time_data[time_name] += issue['fields']['customfield_10016']

        result = dict(sorted(time_data.items()))
        return result
