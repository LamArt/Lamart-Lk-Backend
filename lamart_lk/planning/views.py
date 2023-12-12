import datetime
from datetime import timedelta
from dateutil import tz
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from imaplib import IMAP4, IMAP4_SSL
from caldav import DAVClient, Principal, Event as CalEvent
from caldav.lib.error import NotFoundError
from .serializers import EventDataSerializer, MailCountSerializer, EventCreationSerializer
from icalendar import vDatetime, Event as ICalEvent


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

        return Response(response, status=status.HTTP_200_OK)\
            if len(response) > 0\
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
                rrule['until'] = f'{until_date.year}'\
                                        f'{0 if until_date.month < 10 else ""}'\
                                        f'{until_date.month}'\
                                        f'{0 if until_date.day < 10 else ""}'\
                                        f'{until_date.day}'
            except KeyError:
                pass
            rule_list = [f'{x[0].upper().replace("_", "")}={x[1].upper()}' for x in rrule.items() if x[1]]
            return ';'.join(rule_list)

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

        calendar.add_event(ical=event.to_ical())

        return Response(status=status.HTTP_201_CREATED)

