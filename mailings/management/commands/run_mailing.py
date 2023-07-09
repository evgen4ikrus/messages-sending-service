import logging
import time

from django.core.management.base import BaseCommand

from mailings.models import Client, Mailing, Message

logger = logging.getLogger('mailing')
logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:

            waiting_messages = Message.objects.filter(status='active')

            if not waiting_messages:
                time.sleep(1)
                continue
            
            for message in waiting_messages:
                mailing = message.mailing
                if mailing.status == 'active':
                    clients = Client.objects.filter(
                        tag__in=mailing.client_tags.all(),
                        mobile_operator_code__in=mailing.client_mobile_operator_codes.all()
                    )
                    message.status = 'active'
                    message.save()
                    message_report = send_messages(message, clients, mailing)
                    logger.info(message_report)
                    message.status = 'completed'
                    message.save()


def send_messages(message, clients, mailing):
    text = message.text

    if not clients:
        return f'Нет подходящих номеров для сообщения: {text}.'

    for client in clients:
        mailing = Mailing.objects.get(id=mailing.id)
        if not mailing.status == 'active':
            return f'Отправка сообщений {text} прекращена. Сообщения отправлены не всем пользователям.'

        logger.info(f'Сообщение:"{text}" отправлено клиенту с номером {client.phone_number}')

    return f'Все сообщения: {text} отправлены'
