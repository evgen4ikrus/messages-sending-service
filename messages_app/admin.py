from django.contrib import admin

from .models import Client, Message, MobileOperatorCode, Sending, Tag


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
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
        'mobile_operator_code',
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

    def mobile_operator_code(self, obj):
        return obj.phone_number[1:4]

    mobile_operator_code.short_description = 'Код мобильного оператора'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        MobileOperatorCode.objects.get_or_create(
            mobile_operator_code=obj.phone_number[1:4]
        )
