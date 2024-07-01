from django.contrib.auth.models import User, Group
from . import admin_site
from unfold.admin import ModelAdmin

# Định nghĩa các lớp quản trị tùy chỉnh
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

class CustomGroupAdmin(ModelAdmin):
    pass

# Đăng ký các lớp quản trị với admin site tùy chỉnh
admin_site.register(User, CustomUserAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
admin_site.register(Group, CustomGroupAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
