from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import UserRequest
from django.utils.html import format_html
from django.contrib.admin.actions import delete_selected

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "surname", "phone", "email", "status", "colored_status", "created_at")
    list_editable = ("status",)
    list_filter = (
        'status',
        'created_at',
    )
    search_fields = ("name", "surname", "phone", "email", "orderinfo")
    ordering = ("-id",)
    actions_on_bottom = True

    fieldsets = (
        ("Контактная информация", {
            "fields": ("name", "surname", "phone", "email"),
        }),
        ("Детали заявки", {
            "fields": ("orderinfo", "status"),
        }),
    )

    class Media:
        css = {
            'all': ('css/jazzmin_custom.css',)
        }

    def colored_status(self, obj):
        color_map = {
            'new': 'orange',
            'in_progress': 'dodgerblue',
            'done': 'green',
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 2px 6px; border-radius: 4px;">{}</span>',
            color_map.get(obj.status, 'gray'),
            dict(UserRequest.STATUS_CHOICES).get(obj.status, 'Неизвестно')
        )

    colored_status.short_description = "Статус"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = "Список заявок"
        return super().changelist_view(request, extra_context=extra_context)

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = "Создать заявку"
        return super().add_view(request, form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Редактировать заявку'
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def short_orderinfo(self, obj):
        return (obj.orderinfo[:75] + "...") if len(obj.orderinfo) > 75 else obj.orderinfo

    def has_add_permission(self, request):
        return True
