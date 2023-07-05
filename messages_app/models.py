from django.core.exceptions import ValidationError
from django.db import models


def validate_phone_number(value):
    if not value.startswith('7'):
        raise ValidationError('Номер телефона должен начинаться с цифры "7"')
    if not value.isdigit():
        raise ValidationError('Некорректный номер телефона')
    if len(value) != 11:
        raise ValidationError('Неверное количество цифр в номере')


def validate_mobile_operator_code(value):
    if not value.isdigit():
        raise ValidationError('Некорректный код оператора, он должен состоять из цифр')
    if len(value) != 3:
        raise ValidationError('Код должен состоять из трёх цифр')


class Sending(models.Model):
    start_at = models.DateTimeField(
        'Начать рассылку',
        help_text='Начало отправки сообщений пользователям.',
    )
    end_at = models.DateTimeField(
        'Закончить рассылку',
        help_text='Окончание отправки сообщений пользователям.'
    )
    client_tags = models.ManyToManyField(
        'Tag',
        related_name='sending',
        verbose_name='Теги клиентов',
        help_text='Теги клиентов, которым будет отправлено сообщение.'
    )
    client_mobile_operator_codes = models.ManyToManyField(
        'MobileOperatorCode',
        related_name='sending',
        verbose_name='Коды мобильных операторов клиентов',
        help_text='Коды мобильных операторов клиентов, которым будет отправлено сообщение.'
    )

    def __str__(self):
        return f'{self.id} : {self.start_at} - {self.end_at}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MobileOperatorCode(models.Model):
    mobile_operator_code = models.CharField(
        'Код мобильного оператора',
        max_length=3,
        validators=[validate_mobile_operator_code],
    )

    def __str__(self):
        return self.mobile_operator_code

    class Meta:
        verbose_name = 'Код мобильного оператора'
        verbose_name_plural = 'Коды мобильных операторов'


class Tag(models.Model):
    title = models.CharField(
        'Тег',
        max_length=30,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Client(models.Model):
    phone_number = models.CharField(
        'Номер телефона',
        max_length=11,
        help_text='Номер телефона в формате 7XXXXXXXXXX (X - цифра от 0 до 9)',
        validators=[validate_phone_number],
    )
    tag = models.ForeignKey(
        Tag,
        related_name='clients',
        verbose_name='Тег',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        unique_together = ('phone_number', 'tag')


class Message(models.Model):
    text = models.TextField('Текст')
    create_at = models.DateTimeField('Создано', auto_now_add=True)
    sending = models.ForeignKey(
        Sending,
        related_name='massages',
        verbose_name='Рассылка',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
