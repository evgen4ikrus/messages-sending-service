from django.contrib import admin

from .models import Client, Mailing, Message, MobileOperatorCode, Tag


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = [
        'message',
        'id',
        'start_at',
        'end_at',
        'status',
    ]
    fieldsets = (
        ('Основная информация', {
            'fields': ('message', 'start_at', 'end_at'),
        }),
        ('Фильтры', {
            'fields': ('client_tags', 'client_mobile_operator_codes'),
        }),
    )
    readonly_fields = ('status', )
    # def save_model(self, request, obj, form, change):
    #     obj.message.mailing_id = 
    #     mobile_operator_code, _ = MobileOperatorCode.objects.get_or_create(
    #         code=obj.phone_number[1:4]
    #     )
    #     super().save_model(request, obj, form, change)


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
        'create_at',
    ]
    readonly_fields = ('mailing', 'send_at')


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
