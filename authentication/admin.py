from django.contrib import admin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin



# Định nghĩa các lớp quản trị tùy chỉnh
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    # fieldsets = (
    #     (None, {'fields': ('username', 'email', 'date_joined')}),
    #     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    #     ('Important dates', {'fields': ('last_login',)}),
    # )

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "username",
                    "email",
                    "date_joined",
                ],
            },
        ),
        (
            ("Permissions"),
            {
                "classes": ["tab"],
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ],
            },
        ),
        (
            ("Important dates"),
            {
                "classes": ["tab"],
                "fields": [
                    "last_login",
                ],
            },
        ),
    )

from unfold.admin import TabularInline


class MyInline(TabularInline):
    model = User
    tab = True



class CustomGroupAdmin(ModelAdmin):
    search_fields = ('name',)
    # pass


admin.site.unregister(User)  # Hủy đăng ký mặc định
admin.site.unregister(Group)  # Hủy đăng ký mặc định


admin.site.register(User, CustomUserAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
admin.site.register(Group, CustomGroupAdmin)  # Đăng ký với lớp quản trị tùy chỉnh


