from django.contrib import admin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin



# Định nghĩa các lớp quản trị tùy chỉnh
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )


class CustomGroupAdmin(ModelAdmin):
    search_fields = ('name')
    # pass


# Đăng ký các lớp quản trị với admin site
admin.site.unregister(User)  # Hủy đăng ký mặc định
admin.site.unregister(Group)  # Hủy đăng ký mặc định


admin.site.register(User, CustomUserAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
admin.site.register(Group, CustomGroupAdmin)  # Đăng ký với lớp quản trị tùy chỉnh


# admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from .models import MyModel


@admin.register(MyModel)
class MyModelAdmin(ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": [
                    "field_1",
                    "field_2",
                ],
            },
        ),
        (
            _("Tab 1"),
            {
                "classes": ["tab"],
                "fields": [
                    "field_3",
                    "field_4",
                ],
            },
        ),
        (
            _("Tab 2"),
            {
                "classes": ["tab"],
                "fields": [
                    "field_5",
                    "field_6",
                ],
            },
        ),
    )