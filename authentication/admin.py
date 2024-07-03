from django.contrib import admin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin

# Custom admin classes
class CustomUserAdmin(ModelAdmin):
    actions_list = ['add_to_students_group']
    search_fields = ('username', 'email')  # Ensure these fields are indexed and searchable
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )


class CustomGroupAdmin(ModelAdmin):
    pass

# Unregister the default admin
admin.site.unregister(User)
admin.site.unregister(Group)

# Register custom admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)
