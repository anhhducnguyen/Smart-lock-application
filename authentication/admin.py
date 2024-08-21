from django.contrib import admin
from django.contrib.auth.models import User, Group  
from unfold.admin import ModelAdmin
from django_google_sso.models import GoogleSSOUser

# Định nghĩa các lớp quản trị tùy chỉnh
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

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

class CustomGroupAdmin(ModelAdmin):
    search_fields = ('name',)

class CustomGoogleSSOUserAdmin(ModelAdmin):
    list_display = ('user', 'google_id', 'picture_url', 'locale')
    search_fields = ('user__username', 'google_id', 'locale')
    fieldsets = (
        (None, {'fields': ('user', 'google_id', 'picture_url', 'locale')}),
    )

# Hủy đăng ký các mô hình mặc định nếu cần
admin.site.unregister(User)  # Hủy đăng ký mặc định
admin.site.unregister(Group)  # Hủy đăng ký mặc định

# Đăng ký các mô hình với lớp quản trị tùy chỉnh
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)

# Đăng ký GoogleSSOUser nếu bạn muốn sử dụng mô hình này trong Django Admin
admin.site.register(GoogleSSOUser, CustomGoogleSSOUserAdmin)
