from rest_framework.viewsets import ReadOnlyModelViewSet

from mailings.models import Mailing
from mailings.serializers import MailingSerializer


class MailingView(ReadOnlyModelViewSet):
    queryset = Mailing.objects.all().prefetch_related(
        'client_tags',
        'client_mobile_operator_codes',
    ).select_related('message')
    serializer_class = MailingSerializer

