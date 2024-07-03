from django.contrib import admin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin

# Định nghĩa các lớp quản trị tùy chỉnh
class CustomUserAdmin(ModelAdmin):
    actions_list = ['add_to_students_group']
    search_fields = ('username', 'email')
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

class CustomGroupAdmin(ModelAdmin):
    pass

# Hủy đăng ký admin mặc định
try:
    admin.site.unregister(User)
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass  # Bỏ qua nếu đã bị hủy đăng ký

# Đăng ký admin tùy chỉnh
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)
