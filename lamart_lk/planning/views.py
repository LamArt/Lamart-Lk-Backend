from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from imaplib import IMAP4, IMAP4_SSL

class GetYandexUnreadMailCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
    summary='Get yandex unread mails',
    description='...',
    tags=['planning'],
    )
    def get(self, request):
        username = request.user.email
        access_token = 'y0_AgAAAAAVPIqwAApXyAAAAADwQqCEVoyRNLefRWiCm-LufnvJDUPvY7I'
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