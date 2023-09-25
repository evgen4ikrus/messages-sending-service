from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from mailings.models import Mailing, Client
from mailings.serializers import MailingSerializer, ClientSerializer


class MailingView(ReadOnlyModelViewSet):
    queryset = Mailing.objects.all().prefetch_related(
        'client_tags',
        'client_mobile_operator_codes',
    ).select_related('message')
    serializer_class = MailingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['start_at']


class ClientView(ReadOnlyModelViewSet):
    queryset = Client.objects.all().select_related('tag', 'mobile_operator_code')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['phone_number', 'tag__title']
    filterset_fields = ['mobile_operator_code__code']
