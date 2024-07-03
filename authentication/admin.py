# from django.contrib import admin
# from django.contrib.auth.models import User, Group
# from unfold.admin import ModelAdmin


# # Định nghĩa các lớp quản trị tùy chỉnh
# class CustomUserAdmin(ModelAdmin):
#     list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
#     list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'date_joined')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login',)}),
#     )


# class CustomGroupAdmin(ModelAdmin):
#     pass


# admin.site.unregister(User)  
# admin.site.unregister(Group)  


# admin.site.register(User, CustomUserAdmin)  
# admin.site.register(Group, CustomGroupAdmin) 



# admin.py

from django.db.models import Model
from django.contrib.admin import register
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from unfold.decorators import action


class User(Model):
    pass


@register(User)
class UserAdmin(ModelAdmin):
    actions_list = ["changelist_global_action_import"]
    actions_row = ["changelist_row_action_view_on_website"]
    actions_detail = ["change_detail_action_block"]
    actions_submit_line = ["submit_line_action_activate"]

    @action(description=_("Save & Activate"))
    def submit_line_action_activate(self, request: HttpRequest, obj: User):
        """
        If instance is modified in any way, it also needs to be saved,
        since this handler is invoked after instance is saved.
        :param request:
        :param obj: Model instance that was manipulated, with changes already saved to database
        :return: None, this handler should not return anything
        """
        obj.is_active = True
        obj.save()

    @action(description=_("Import"), url_path="import")
    def changelist_global_action_import(self, request: HttpRequest):
        """
        Handler for global actions does not receive any queryset or object ids, because it is
        meant to be used for general actions for given model.
        :param request:
        :return: View, as described in section above
        """
        # This is example of action redirecting to custom page, where the action will be handled
        # (with intermediate steps)
        return redirect(
          reverse_lazy("view-where-import-will-be-handled")
        )

    @action(description=_("Row"), url_path="row-action", attrs={"target": "_blank"})
    def changelist_row_action_view_on_website(self, request: HttpRequest, object_id: int):
        """
        Handler for list row action.
        :param request:
        :param object_id: ID of instance that this action was invoked for
        :return: View, as described in section above
        """
        return redirect(f"https://example.com/{object_id}")

    @action(description=_("Detail"), url_path="detail-action", attrs={"target": "_blank"})
    def change_detail_action_block(self, request: HttpRequest, object_id: int):
        """
        Handler for detail action.
        :param request:
        :param object_id: ID of instance that this action was invoked for
        :return: View, as described in section above
        """
        # This is example of action that handled whole logic inside handler
        # function and redirects back to object detail
        user = User.objects.get(pk=object_id)
        user.block()
        return redirect(
            reverse_lazy("admin:users_user_change", args=(object_id,))
        )