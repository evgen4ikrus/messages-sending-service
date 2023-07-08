from rest_framework import serializers

from .models import Client, Mailing, Message, MobileOperatorCode, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'create_at', 'mailing', 'status']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'phone_number', 'tag', 'mobile_operator_code', ]


class MobileOperatorCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileOperatorCode
        fields = ['id', 'code']


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ['id', 'start_at', 'end_at', 'client_tags', 'client_mobile_operator_codes']
