from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from mailings.models import Client, Mailing, Message, MobileOperatorCode, Tag
from mailings.serializers import (ClientSerializer, MailingSerializer,
                                  MessageSerializer,
                                  MobileOperatorCodeSerializer, TagSerializer)


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mobile_operator_code', 'tag']


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MobileOperatorCodeList(generics.ListCreateAPIView):
    queryset = MobileOperatorCode.objects.all()
    serializer_class = MobileOperatorCodeSerializer


class MobileOperatorCodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MobileOperatorCode.objects.all()
    serializer_class = MobileOperatorCodeSerializer


class MailingList(generics.ListCreateAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
