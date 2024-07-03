from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django_google_sso.models import GoogleSSOUser

# Định nghĩa các lớp quản trị tùy chỉnh
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

class CustomGroupAdmin(GroupAdmin):
    pass

class CustomGoogleSSOUserAdmin(admin.ModelAdmin):
    pass

# Đăng ký các lớp quản trị với admin site
admin.site.unregister(User)  # Hủy đăng ký mặc định
admin.site.unregister(Group)  # Hủy đăng ký mặc định
# Nếu GoogleSSOUser chưa được đăng ký trước đó, không cần hủy đăng ký
# admin.site.unregister(GoogleSSOUser)  # Đảm bảo rằng GoogleSSOUser đã được đăng ký trước đó mới hủy đăng ký

admin.site.register(User, CustomUserAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
admin.site.register(Group, CustomGroupAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
admin.site.register(GoogleSSOUser, CustomGoogleSSOUserAdmin)
