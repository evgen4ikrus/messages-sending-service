from django.contrib import admin

from .models import Client, Message, MobileOperatorCode, Mailing, Tag
from .services.messages_sending_service import prepare_messages


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'start_at',
        'end_at',
    ]
    fieldsets = (
        ('Основная информация', {
            'fields': ('start_at', 'end_at'),
        }),
        ('Фильтры', {
            'fields': ('client_tags', 'client_mobile_operator_codes'),
        }),
    )


@admin.register(MobileOperatorCode)
class MobileOperatorCodeAdmin(admin.ModelAdmin):
    list_display = [
        'code',
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        'title',
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'text',
        'status',
    ]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'phone_number',
        'tag',
        'mobile_operator_code',
    ]
    readonly_fields = ('mobile_operator_code',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('phone_number', 'tag', 'mobile_operator_code'),
        }),
    )

    def save_model(self, request, obj, form, change):
        mobile_operator_code, _ = MobileOperatorCode.objects.get_or_create(
            code=obj.phone_number[1:4]
        )
        obj.mobile_operator_code = mobile_operator_code
        super().save_model(request, obj, form, change)
