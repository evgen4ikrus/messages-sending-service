from django.contrib import admin

from .models import Client, Message, Sending


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'start_at',
        'end_at',
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'text',
    ]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'phone_number',
        'tag',
    ]

# mobile_operator_code = models.CharField(
#     'Код мобильного оператора',
#     max_length=3,
# )
