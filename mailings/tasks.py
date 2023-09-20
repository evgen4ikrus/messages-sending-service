import logging
import time
from datetime import datetime

from celery import shared_task

from .models import Client, Mailing

logger = logging.getLogger('mailing')
logging.basicConfig(level=logging.INFO)


@shared_task()
def run_mailing(mailing_id):
    time.sleep(3) # FIX: заменить на что-то более правильное
    mailing = Mailing.objects.get(id=mailing_id)

    if mailing.end_at <= datetime.now():
        mailing.status = 'completed'
        mailing.save()
        return

    if mailing.start_at <= datetime.now():
        mailing.status = 'active'
        mailing.save()

    mailing_status = mailing.status

    if mailing_status == 'waiting':
        time.sleep(10)
        run_mailing.delay(mailing_id)
        return

    clients = Client.objects.filter(
        tag__in=mailing.client_tags.all(),
        mobile_operator_code__in=mailing.client_mobile_operator_codes.all()
    )
    mailing_report = send_messages(clients, mailing)
    logger.info(mailing_report)
    mailing.status = 'completed'
    mailing.save()
    mailing.message.send_at = datetime.now()
    mailing.message.save()


def send_messages(clients, mailing):
    text = mailing.message.text

    if not clients:
        return f'Нет подходящих номеров для сообщения: "{text}".'

    for client in clients:
        time.sleep(1)
        mailing = Mailing.objects.get(id=mailing.id)
        if not mailing.ready_to_send:
            return f'Отправка сообщений "{text}" прекращена. Сообщения отправлены не всем пользователям.'

        logger.info(f'Сообщение:"{text}" отправлено клиенту с номером {client.phone_number}')
    return f'Все сообщения: "{text}" отправлены'
