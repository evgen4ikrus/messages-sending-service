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


MESSAGE_STATUSES = [
    ('waiting', 'Ожидает рассылки'),
    ('active', 'Активная рассылка'),
    ('completed', 'Рассылка завершена'),
]


class Mailing(models.Model):
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
        related_name='mailings',
        verbose_name='Теги клиентов',
        help_text='Теги клиентов, которым будет отправлено сообщение.'
    )
    client_mobile_operator_codes = models.ManyToManyField(
        'MobileOperatorCode',
        related_name='mailings',
        verbose_name='Коды мобильных операторов клиентов',
        help_text='Коды мобильных операторов клиентов, которым будет отправлено сообщение.'
    )

    def __str__(self):
        return f'{self.id} : {self.start_at} - {self.end_at}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MobileOperatorCode(models.Model):
    code = models.CharField(
        'Код мобильного оператора',
        max_length=3,
        validators=[validate_mobile_operator_code],
    )

    def __str__(self):
        return self.code

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
    mobile_operator_code = models.ForeignKey(
        MobileOperatorCode,
        related_name='clients',
        verbose_name='Код мобильного оператора',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='Заполняется автоматически, после сохранения данных'
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
    mailing = models.ForeignKey(
        Mailing,
        related_name='massages',
        verbose_name='Рассылка',
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=MESSAGE_STATUSES,
        help_text='Присваивается автоматически.'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
