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
    search_fields = ('name',)
    # pass


admin.site.unregister(User)  # Hủy đăng ký mặc định
admin.site.unregister(Group)  # Hủy đăng ký mặc định


admin.site.register(User, CustomUserAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
admin.site.register(Group, CustomGroupAdmin)  # Đăng ký với lớp quản trị tùy chỉnh


# from django.contrib import admin
# from django.contrib.auth.models import User, Group
# from unfold.admin import ModelAdmin, Tab

# # Định nghĩa các lớp quản trị tùy chỉnh
# class CustomUserAdmin(ModelAdmin):
#     tabs = [
#         Tab(label='Thông tin người dùng', url='/admin/auth/user/'),
#         Tab(label='Nhóm người dùng', url='/admin/auth/group/'),
#         Tab(label='Người dùng đang hoạt động', url='/admin/auth/user/?is_active__exact=1'),
#         Tab(label='Người dùng không hoạt động', url='/admin/auth/user/?is_active__exact=0'),
#     ]
#     list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
#     list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
#     search_fields = ('username', 'email')
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'date_joined')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login',)}),
#     )

# class CustomGroupAdmin(ModelAdmin):
#     search_fields = ('name',)

# # Đăng ký các lớp quản trị với admin site
# admin.site.unregister(User)  # Hủy đăng ký mặc định
# admin.site.unregister(Group)  # Hủy đăng ký mặc định

# admin.site.register(User, CustomUserAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
# admin.site.register(Group, CustomGroupAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
