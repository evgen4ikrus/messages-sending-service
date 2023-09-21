from rest_framework import serializers

from .models import Mailing, Message, MobileOperatorCode, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MobileOperatorCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileOperatorCode
        fields = '__all__'


class MailingSerializer(serializers.ModelSerializer):
    client_tags = TagSerializer(many=True)
    message = MessageSerializer()
    client_mobile_operator_codes = MobileOperatorCodeSerializer(many=True)

    class Meta:
        model = Mailing
        fields = ('message', 'start_at', 'end_at', 'client_tags', 'client_mobile_operator_codes', 'status')
