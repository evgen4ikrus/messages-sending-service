# Generated by Django 3.2.16 on 2023-09-20 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0004_remove_message_mailing_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('waiting', 'Ожидание'), ('active', 'В процессе'), ('completed', 'Завершена')], default='waiting', help_text='Присваивается автоматически.', max_length=20, verbose_name='Статус'),
        ),
    ]