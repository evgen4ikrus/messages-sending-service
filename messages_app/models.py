from django.core.exceptions import ValidationError
from django.db import models


def validate_phone_number(value):
    if not value.startswith('7'):
        raise ValidationError('Номер телефона должен начинаться с цифры "7"')
    if not value.isdigit():
        raise ValidationError('Некорректный номер телефона')
    if len(value) != 11:
        raise ValidationError('Неверное количество цифр в номере')


class Sending(models.Model):
    start_at = models.DateTimeField(
        'Начать рассылку',
        help_text='Начало отправки сообщений пользователям.',
    )
    end_at = models.DateTimeField(
        'Закончить рассылку',
        help_text='Окончание отправки сообщений пользователям.'
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class Client(models.Model):
    phone_number = models.CharField(
        'Номер телефона',
        max_length=11,
        unique=True,
        help_text='Номер телефона в формате 7XXXXXXXXXX (X - цифра от 0 до 9)',
        validators=[validate_phone_number],
    )
    tag = models.CharField(
        'Тег',
        max_length=30,
        blank=True,
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    text = models.TextField('Текст')
    create_at = models.DateTimeField('Создано', auto_now_add=True)
    sending = models.ForeignKey(
        Sending,
        related_name='massages',
        verbose_name='Рассылка',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
