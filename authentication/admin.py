from django.contrib import admin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin

# Định nghĩa các lớp quản trị tùy chỉnh
class CustomUserAdmin(ModelAdmin):
    pass

class CustomGroupAdmin(ModelAdmin):
    pass

# Đăng ký các lớp quản trị với admin site
admin.site.unregister(User)  # Hủy đăng ký mặc định
admin.site.unregister(Group)  # Hủy đăng ký mặc định

admin.site.register(User, CustomUserAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
admin.site.register(Group, CustomGroupAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
