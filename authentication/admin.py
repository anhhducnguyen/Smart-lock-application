from django.contrib import admin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin

# Định nghĩa các lớp quản trị tùy chỉnh
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )


class CustomGroupAdmin(ModelAdmin):
    pass


# Danh sách thông tin người dùng
users_info = [
    {'username': 'john', 'password': 'pass1234', 'email': 'john@example.com'},
    {'username': 'jane', 'password': 'pass5678', 'email': 'jane@example.com'},
    {'username': 'alice', 'password': 'pass91011', 'email': 'alice@example.com'},
    # Thêm người dùng khác ở đây
]

# Tạo người dùng từ danh sách
for user_info in users_info:
    user = User.objects.create_user(
        username=user_info['username'],
        password=user_info['password'],
        email=user_info['email']
    )
    user.save()


# Đăng ký các lớp quản trị với admin site
admin.site.unregister(User)  # Hủy đăng ký mặc định
admin.site.unregister(Group)  # Hủy đăng ký mặc định

admin.site.register(User, CustomUserAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
admin.site.register(Group, CustomGroupAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
