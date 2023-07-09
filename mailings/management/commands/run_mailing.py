import logging
import time

from django.core.management.base import BaseCommand

from mailings.models import Message, Client, Mailing

logger = logging.getLogger('messages_sending_service')
logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = 'The Zen of Python'

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
                    send_messages(message, clients, mailing)


def send_messages(message, clients, mailing):
    text = message.text
    
    for client in clients:
        mailing = Mailing.objects.get(id=mailing.id)
        if not mailing.status == 'active':
            logger.info(f'Отправка сообщений: "{text}" завершена. Сообщения отправлены не всем пользователям.')
            message.status = 'completed'
            message.save()
            return

        logger.info(f'Сообщение:"{text}" отправлено клиенту с номером {client.phone_number}')
        time.sleep(10)

    logger.info(f'Сообщение: "{text}" отправлено всем необходимым пользователям')
    message.status = 'completed'
    message.save()
