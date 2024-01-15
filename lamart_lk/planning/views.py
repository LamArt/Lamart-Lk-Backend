import datetime
from datetime import timedelta
from dateutil import tz
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from imaplib import IMAP4, IMAP4_SSL
from caldav import DAVClient, Principal, Event as CalEvent
from caldav.lib.error import NotFoundError
from .serializers import EventDataSerializer, MailCountSerializer, EventCreationSerializer, IssueDataSerializer
from icalendar import vDatetime, Event as ICalEvent, vCalAddress
from salary.utils.salary import SalaryStoryPoints
from django.db.models import ObjectDoesNotExist


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

        today = datetime.datetime.utcnow().date()
        start = datetime.datetime(today.year, today.month, today.day, tzinfo=tz.tzlocal())
        end = start + timedelta(1)

        try:
            calendars = principal.calendars()
        except NotFoundError:
            return Response('Calendars do not exist', status=status.HTTP_404_NOT_FOUND)
        response = {}

        for calendar in calendars:
            for raw_event in calendar.search(comp_class=CalEvent, start=start, end=end):
                event_info = {}
                event = raw_event.vobject_instance.vevent

                event_info['title'] = str(event.summary.value)
                try:
                    event_info['description'] = str(event.description.value)
                except AttributeError:
                    event_info['description'] = None
                event_info['start_time'] = str(event.dtstart.value)
                event_info['end_time'] = str(event.dtend.value)
                event_info['url'] = str(event.url.value)

                response[str(event.uid.value)] = event_info

                response = dict(sorted(response.items(), key=lambda item: item[1]['start_time'].split(' ')[1]))

        return Response(response, status=status.HTTP_200_OK) \
            if len(response) > 0 \
            else Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=EventCreationSerializer,
        summary='Add new event',
        description='Takes calendar\'s data, creates new event to yandex calendar',
        tags=['planning'],
    )
    def post(self, request):
        def get_rrule_string(rrule):
            try:
                until_date = datetime.datetime.fromisoformat(rrule['until'])
                rrule['until'] = f'{until_date.year}' \
                                 f'{0 if until_date.month < 10 else ""}' \
                                 f'{until_date.month}' \
                                 f'{0 if until_date.day < 10 else ""}' \
                                 f'{until_date.day}'
            except KeyError:
                pass
            rule_list = [f'{x[0].upper().replace("_", "")}={x[1].upper()}' for x in rrule.items() if x[1]]
            return ';'.join(rule_list)

        def send_invites():
            attendees = request.data['attendees']

            organizer = vCalAddress(f'MAILTO:{request.user.email}')
            event['organizer'] = organizer

            if isinstance(attendees, type([])):
                for attendee_email in attendees:
                    attendee = vCalAddress(f'MAILTO:{attendee_email}')
                    event.add('attendee', attendee, encode=0)
            else:
                attendee = vCalAddress(f'MAILTO:{attendees}')
                event.add('attendee', attendee, encode=0)

        principal = get_caldav_principal(request)

        try:
            calendar = principal.calendars()[0]
        except NotFoundError:
            return Response('Calendars do not exist', status=status.HTTP_404_NOT_FOUND)

        event = ICalEvent()
        try:
            event['summary'] = request.data['title'] if request.data['title'] else 'Без названия'
        except KeyError:
            return Response('Could not find \'title\' in request body', status=status.HTTP_400_BAD_REQUEST)

        try:
            event['dtstart'] = vDatetime(datetime.datetime.fromisoformat(request.data['start_time']))
        except KeyError:
            return Response('Could not find \'start_time\' in request body', status=status.HTTP_400_BAD_REQUEST)

        try:
            event['dtend'] = vDatetime(datetime.datetime.fromisoformat(request.data['end_time']))
        except KeyError:
            return Response('Could not find \'end_time\' in request body', status=status.HTTP_400_BAD_REQUEST)

        try:
            event['description'] = request.data['description']
        except KeyError:
            pass

        try:
            event['rrule'] = get_rrule_string(request.data['rrule'])
        except KeyError:
            pass

        try:
            event['x-telemost-required'] = request.data['create_conference']
        except KeyError:
            return Response('Could not find \'create_conference\' in request body', status=status.HTTP_400_BAD_REQUEST)

        if 'attendees' in request.data.keys():
            send_invites()
        calendar.add_event(ical=event.to_ical())

        return Response(status=status.HTTP_201_CREATED)


class AtlassianJiraIssuesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary='Get Jira issues',
        responses=IssueDataSerializer,
        description='Returns uncompleted Jira issues sorted by priority',
        tags=['planning'],
    )
    def get(self, request):
        def convert_issue_data(data):
            def return_issue_info(issue):
                issue_info = {}
                issue_info['title'] = issue['fields']['summary']
                issue_info['priority'] = {
                    'name': issue['fields']['priority']['name'],
                    'id': str(issue['fields']['priority']['id'])
                }
                issue_info['story_points'] = issue['fields']['customfield_10052']

                if not (issue['fields']['description']):
                    issue_info['description'] = None
                else:
                    all_text = []
                    for content in issue['fields']['description']['content']:
                        all_content_text = []
                        for sub_content in content['content']:
                            try:
                                all_text.append(sub_content['text'])
                            except KeyError:
                                issue_info['description'] = None
                                return issue_info

                        all_text.append(' '.join(all_content_text))
                        all_content_text.clear()
                    issue_info['description'] = '\r\n'.join(all_text)

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
                if not ('parent' in issue['fields'].keys()):
                    continue
                issue_info = return_issue_info(issue)
                response_data[issue['fields']['parent']['key']]['subtasks'].append(issue_info)

            return dict(sorted(response_data.items(), key=lambda item: item[1]['priority']['id']))

        def return_issues_data_from_jira():
            try:
                refresh = request.user.provider_tokens.get(provider='atlassian').refresh_token
            except ObjectDoesNotExist:
                return Response('User does not authorized in Atlassian', status=status.HTTP_401_UNAUTHORIZED)

            atlassian_user = SalaryStoryPoints(refresh, request.user)
            query_of_projects = ' OR '.join(
                [f'project="{project}"' for project in atlassian_user.project_manager.get_jira_keys()])
            if not query_of_projects:
                return Response('User does not belong to any team', status=status.HTTP_404_NOT_FOUND)

            jql_query = f'({query_of_projects})' \
                        f' AND assignee=currentUser()' \
                        f' AND statusCategory IN (2, 4)'
            params = {
                'jql': jql_query,
                'fields': 'priority, summary, description, parent, customfield_10052',
                'maxResults': 100000,
            }

            rq = requests.get(f'{atlassian_user.search_url}/search', params=params, headers=atlassian_user.headers)
            if rq.status_code == 200:
                return rq.json()
            return Response(rq.json(), status=rq.status_code)

        data = return_issues_data_from_jira()
        if isinstance(data, Response):
            return data

        return Response(convert_issue_data(data), status=status.HTTP_200_OK)
