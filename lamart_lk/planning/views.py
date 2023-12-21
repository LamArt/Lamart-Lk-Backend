import datetime
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from imaplib import IMAP4, IMAP4_SSL
from caldav import DAVClient, Principal
from caldav.lib.error import NotFoundError
from .serializers import EventDataSerializer, MailCountSerializer, IssueDataSerializer


def get_caldav_principal(request_body) -> Principal:
    username = request_body.user.email
    url = f'https://caldav.yandex.ru/calendars/{username}/'
    access_token = request_body.user.provider_tokens.get(provider='yandex').access_token

    client = DAVClient(url=url, username=username, password=access_token)
    principal = client.principal()
    return principal


class YandexUnreadMailCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
    summary='Get mail count',
    responses=MailCountSerializer,
    description='Returns yandex unread mails count',
    tags=['planning'],
    )
    def get(self, request):
        username = request.user.email
        access_token = request.user.provider_tokens.get(provider='yandex').access_token
        auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
        imap_connector = IMAP4_SSL('imap.yandex.com', 993)
        try:
            imap_connector.authenticate('XOAUTH2', lambda x: auth_string)
        except IMAP4.error:
            response = 'Could not establish connection. Check IMAP connection permission in personal account'
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        imap_connector.select('INBOX')
        imap_status, imap_response = imap_connector.search(None, '(UNSEEN)')
        mail_count = len(imap_response[0].split())
        imap_connector.close()
        imap_connector.logout()
        response = {'count': mail_count}
        return Response(response, status=status.HTTP_200_OK)


class YandexCalendarEventsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
    summary='Get today\'s events',
    responses=EventDataSerializer,
    description='Returns yandex today\'s calendar events',
    tags=['planning'],
    )
    def get(self, request):
        principal = get_caldav_principal(request)

        try:
            calendars = principal.calendars()
        except NotFoundError:
            return Response('Calendars do not exist', status=status.HTTP_404_NOT_FOUND)
        response = {}
        date = str(datetime.date.today())
        for calendar in calendars:
            for raw_event in calendar.events():
                event_info = {}
                event = raw_event.vobject_instance.vevent

                if date not in str(event.dtstart.value):
                     continue
                event_info['title'] = str(event.summary.value)
                try:
                    description = " ".join(str(event.description.value).replace('\n', ' ').split())
                    event_info['description'] = description
                except AttributeError:
                    event_info['description'] = None
                event_info['start_time'] = str(event.dtstart.value)
                event_info['end_time'] = str(event.dtend.value)
                event_info['url'] = str(event.url.value)

                response[str(event.uid.value)] = event_info

        return Response(response, status=status.HTTP_200_OK)\
            if len(response) > 0\
            else Response(status=status.HTTP_204_NO_CONTENT)


class AtlassianJiraIssuesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        summary='Get Jira issues',
        responses=IssueDataSerializer,
        description='Returns uncompleted Jira issues sorted by priority',
        tags=['planning'],
    )
    def get(self, request):
        def return_issues_data_from_jira():
            accessible_resource = 'https://api.atlassian.com/oauth/token/accessible-resources'
            base_url = 'https://api.atlassian.com/ex/jira/'
            access_token = request.user.provider_tokens.get(provider='atlassian').access_token
            headers = {'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}

            rq = requests.get(url=accessible_resource, headers=headers)
            if rq.status_code == 200:
                cloud_id = rq.json()[0]['id']
            else:
                return Response(rq.json(), status=rq.status_code)

            search_url = f"{base_url}{cloud_id}/rest/api/3/"
            rq = requests.get(f'{search_url}/project', headers=headers)
            if rq.status_code == 200:
                projects_data = rq.json()
                projects = [project_info['key'] for project_info in projects_data if 'key' in project_info]
            else:
                return Response(rq.json(), status=rq.status_code)

            query_of_projects = ' OR '.join([f'project={project}' for project in projects])
            jql_query = f'({query_of_projects})' \
                        f' AND assignee=currentUser()' \
                        f' AND statusCategory IN (2, 4)' \

            params = {
                'jql': jql_query,
                'fields': 'status, priority, summary, description, parent',
                'maxResults': 100000,
            }
            rq = requests.get(f'{search_url}/search', params=params, headers=headers)
            if rq.status_code == 200:
                return rq.json()
            return Response(rq.json(), status=rq.status_code)

        def convert_issue_data(data):
            def return_issue_info(issue):
                issue_info = {}
                issue_info['title'] = issue['fields']['summary']
                if not (issue['fields']['description']):
                    issue_info['description'] = issue['fields']['description']
                else:
                    all_text = []
                    for content in issue['fields']['description']['content']:
                        all_content_text = []
                        for sub_content in content['content']:
                            all_text.append(sub_content['text'])
                        all_text.append(' '.join(all_content_text))
                        all_content_text.clear()
                    issue_info['description'] = '\r\n'.join(all_text)

                issue_info['priority'] = {
                    'name': issue['fields']['priority']['name'],
                    'id': str(issue['fields']['priority']['id'])
                }
                return issue_info

            response_data = {}
            issues = data['issues']
            for issue in issues:
                if 'parent' in issue['fields'].keys():
                    continue
                issue_info = return_issue_info(issue)
                issue_info['subtasks'] = []
                response_data[issue['key']] = issue_info

            for issue in issues:
                if not('parent' in issue['fields'].keys()):
                    continue
                issue_info = return_issue_info(issue)
                response_data[issue['fields']['parent']['key']]['subtasks'].append(issue_info)

            return dict(sorted(response_data.items(), key=lambda item: item[1]['priority']['id']))

        data = return_issues_data_from_jira()
        if isinstance(data, Response):
            return data

        return Response(convert_issue_data(data), status=status.HTTP_200_OK)

