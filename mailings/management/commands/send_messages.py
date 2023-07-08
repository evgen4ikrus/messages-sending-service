import logging
import time
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from ...apy_methods import (create_message, delete_message, get_clients,
                            get_mailing_by_id, get_messages_by_status)

logger = logging.getLogger('messages_sending_service')
logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        host = settings.HOST_NAME

        while True:

            waiting_messages = get_messages_by_status(host, 'waiting')
            if not waiting_messages:
                time.sleep(1)
                continue

            for message in waiting_messages:
                current_message_status = message.get('status')
                actual_message_status = get_message_status(host, message)
                if current_message_status != actual_message_status:
                    message = update_message(host, message, actual_message_status)
                    if message.get('status') == 'active':
                        send_messages(host, message)


def get_message_status(host, message):
    mailing = get_mailing_by_id(host, message.get('mailing'))
    mailing_start = datetime.strptime(mailing.get('start_at'), "%Y-%m-%dT%H:%M:%S")
    mailing_end = datetime.strptime(mailing.get('end_at'), "%Y-%m-%dT%H:%M:%S")
    now = datetime.now()
    if mailing_end < now:
        return 'completed'
    if mailing_start < now:
        return 'active'
    return 'waiting'


def send_messages(host, message):
    text = message.get('text')
    mailing = get_mailing_by_id(host, message.get('mailing'))
    for code in mailing.get('client_mobile_operator_codes'):
        for tag in mailing.get('client_tags'):
            clients = get_clients(host, tag, code)
            if not clients:
                continue
            for client in clients:
                actual_message_status = get_message_status(host, message)
                if actual_message_status == 'completed':
                    logger.info(f'Отправка сообщений: "{text}" завершено. Сообщения отправлены не всем пользователям. '
                                'Время окончания рассылки меньше текущего.')
                    return
                if actual_message_status == 'waiting':
                    logger.info(f'Отправка сообщений: "{text}" завершено. Сообщения отправлены не всем пользователям. '
                                'Время начала рассылки больше текущего.')
                    return
                logger.info(f'Сообщение:"{text}" отправлено клиенту с номером {client.get("phone_number")}')
    logger.info(f'Сообщение: "{text}" отправлено всем необходимым пользователям')


# FIXME: Изменить на метод update
def update_message(host, message, status):
    delete_message(host, message.get('id'))
    message = create_message(
        host,
        message.get('id'),
        message.get('text'),
        message.get('mailing'),
        message.get('create_at'),
        status,
    )
    return message
