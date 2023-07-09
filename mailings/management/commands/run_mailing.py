import datetime
import logging
import random
import time

from django.core.management.base import BaseCommand

from mailings.models import Client, Mailing, Message, Tag, MobileOperatorCode

logger = logging.getLogger('mailing')
logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):

    def handle(self, *args, **options):

        while True:

            for mailing in Mailing.objects.filter(status=''):
                mailing.status = 'waiting'
                mailing.save()
            
            waiting_mailings = Mailing.objects.filter(status='waiting')

            if not waiting_mailings:
                continue
            
            for mailing in waiting_mailings:
                if mailing.ready_to_send:
                    mailing.status = 'active'
                    mailing.save()
                    clients = Client.objects.filter(
                        tag__in=mailing.client_tags.all(),
                        mobile_operator_code__in=mailing.client_mobile_operator_codes.all()
                    )
                    message_report = send_messages(clients, mailing)
                    logger.info(message_report)
                    mailing.status = 'completed'
                    mailing.save()
            time.sleep(1)

def send_messages(clients, mailing):
    text = mailing.message.text

    if not clients:
        return f'Нет подходящих номеров для сообщения: {text}.'

    for client in clients:
        mailing = Mailing.objects.get(id=mailing.id)
        if not mailing.ready_to_send:
            return f'Отправка сообщений {text} прекращена. Сообщения отправлены не всем пользователям.'
        logger.info(f'Сообщение:"{text}" отправлено клиенту с номером {client.phone_number}')
    return f'Все сообщения: {text} отправлены'
