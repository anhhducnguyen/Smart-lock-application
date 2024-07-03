from django.contrib import admin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin
from django_google_sso.models import GoogleSSOUser

# Định nghĩa các lớp quản trị tùy chỉnh
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

class GoogleSSOUserAdmin(ModelAdmin):
    list_display = ('google_id',)  # Adjust fields as needed


class CustomGroupAdmin(ModelAdmin):
    pass





# Đăng ký các lớp quản trị với admin site
admin.site.unregister(User)  # Hủy đăng ký mặc định
admin.site.unregister(Group)  # Hủy đăng ký mặc định

admin.site.register(User, CustomUserAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
admin.site.register(Group, CustomGroupAdmin)  # Đăng ký với lớp quản trị tùy chỉnh


# Register the GoogleSSOUser model with the custom admin class
admin.site.register(GoogleSSOUser, GoogleSSOUserAdmin)