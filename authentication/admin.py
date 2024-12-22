from django.utils.timezone import now, timedelta
from pyexpat.errors import messages
import random
from django.contrib import admin
from django.contrib.auth.models import User, Group  
from unfold.admin import ModelAdmin
from django_google_sso.models import GoogleSSOUser
from django.templatetags.static import static
from unfold.decorators import action, display
from django.urls import path, reverse_lazy
from unfold.components import BaseComponent, register_component
from authentication.sites import authentication_admin_site
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    RangeDateFilter,
    RangeNumericFilter,
    SingleNumericFilter,
    TextFilter,
)
from django.core.validators import EMPTY_VALUES
from django.db.models import Q

from authentication import models
from unfold.contrib.forms.widgets import WysiwygWidget

from authentication.views import MyStore, MyStatistical



class FullNameFilter(TextFilter):
    title = ("username")
    parameter_name = "username"

    def queryset(self, request, queryset):
        if self.value() in EMPTY_VALUES:
            return queryset

        return queryset.filter(
            Q(first_name__icontains=self.value()) | Q(last_name__icontains=self.value())
        )
    
class GreaterSalaryFilter(TextFilter):
    title = "Salary (greater than)"  # Tiêu đề của bộ lọc
    parameter_name = "salary"

    def queryset(self, request, queryset):
        # Kiểm tra nếu không có giá trị được nhập
        if self.value() in [None, ""]:
            return queryset

        try:
            # Chuyển giá trị nhập vào thành số và lọc
            salary_value = float(self.value())
            return queryset.filter(salary__gt=salary_value)
        except ValueError:
            # Nếu nhập không phải là số, trả về queryset ban đầu
            return queryset

class LessSalaryFilter(TextFilter):
    title = "Salary (less than)"  # Tiêu đề của bộ lọc
    parameter_name = "salary"

    def queryset(self, request, queryset):
        # Kiểm tra nếu không có giá trị được nhập
        if self.value() in [None, ""]:
            return queryset

        try:
            # Chuyển giá trị nhập vào thành số và lọc
            salary_value = float(self.value())
            return queryset.filter(salary__lt=salary_value)
        except ValueError:
            # Nếu nhập không phải là số, trả về queryset ban đầu
            return queryset


# Định nghĩa các lớp quản trị tùy chỉnh
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    # fieldsets = (
    #     (None, {'fields': ('username', 'email', 'date_joined')}),
    #     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    #     ('Important dates', {'fields': ('last_login',)}),
    # )

    list_filter = [
        FullNameFilter,
        ("is_active", ChoicesDropdownFilter),
    ]
    list_filter_submit = True
    list_fullwidth = True

    # fieldsets = (
    #     (
    #         None,
    #         {
    #             "fields": [
    #                 "username",
    #                 "email",
    #                 "date_joined",
    #             ],
    #         },
    #     ),
    #     (
    #         ("Permissions"),
    #         {
    #             "classes": ["tab"],
    #             "fields": [
    #                 "is_active",
    #                 "is_staff",
    #                 "is_superuser",
    #                 "groups",
    #                 "user_permissions",
    #             ],
    #         },
    #     ),
    #     (
    #         ("Important dates"),
    #         {
    #             "classes": ["tab"],
    #             "fields": [
    #                 "last_login",
    #             ],
    #         },
    #     ),
    # )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    # formfield_overrides = {
    #     models.TextField: {
    #         "widget": WysiwygWidget,
    #     }
    # }
    readonly_fields = ["last_login", "date_joined"]

    @display(description=("User"))
    def display_header(self, instance: User):
        return instance.username

    @display(description=("Staff"), boolean=True)
    def display_staff(self, instance: User):
        return instance.is_staff

    @display(description=("Superuser"), boolean=True)
    def display_superuser(self, instance: User):
        return instance.is_superuser

    @display(description=("Created"))
    def display_created(self, instance: User):
        return instance.created_at

from unfold.admin import TabularInline


class MyInline(TabularInline):
    model = User
    tab = True



# class CustomGroupAdmin(ModelAdmin):
#     search_fields = ('name',)

@admin.register(Group, site=authentication_admin_site)
class CustomGroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

   
# class CustomGoogleSSOUserAdmin(ModelAdmin):
#     list_display = ('user', 'google_id', 'picture_url', 'locale')
#     search_fields = ('user__username', 'google_id', 'locale')
#     fieldsets = (
#         (None, {'fields': ('user', 'google_id', 'picture_url', 'locale')}),
#     )



from django.contrib import admin
from .models import Employee, Status, UserProfile
from firebase_admin import storage
from django.utils.html import format_html

# Hàm để lấy URL của ảnh đầu tiên từ Firebase
def get_first_image_url_from_firebase(user_name):
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix=f'images/{user_name}/')
    
    for blob in blobs:
        parts = blob.name.split('/')
        if parts[-1] == '0.jpg':  # Kiểm tra nếu đây là ảnh đầu tiên
            return blob.public_url
    return None

from unfold import admin as unfold_admin
from django.utils.html import mark_safe

# class CustomGoogleSSOUserAdmin(unfold_admin.ModelAdmin):
#     list_display = ('user', 'google_id', 'picture_url', 'locale')

class UserProfileAdmin(unfold_admin.ModelAdmin):
    list_display = ('display_picture', 'name', 'age', 'sex', 'date_join', 'email', "display_status",)  # Hiển thị tên và ảnh đầu tiên
    # list_display = ('picture', 'name', 'age', 'sex', 'date_join', 'email', "display_status",)
    search_fields = ('name',)  # Tìm kiếm theo tên (chú ý dấu phẩy để định nghĩa tuple)
    list_filter = ('name', 'age', 'sex', 'date_join', 'email')

    search_fields = ('name', 'email',)

    list_filter = [
        FullNameFilter,
        ("data", ChoicesDropdownFilter),
        ("date_join", RangeDateFilter),
    ]
    list_filter_submit = True
    list_fullwidth = True
    # change_list_template = "train/button_form.html"

    

    def display_picture(self, obj):
        if obj.picture:
            return mark_safe(f'<img src="{obj.picture.url}" style="width: 70px; height: 70px; border-radius: 50%;" />')
        return '-'
    
    # Đặt tiêu đề cho cột ảnh
    display_picture.short_description = 'Picture'

    @display(
        description=("Status"),
        label={
            Status.INACTIVE: "danger",
            Status.ACTIVE: "success",
        },
    )
    def display_status(self, instance: UserProfile):
        if instance.data:
            return instance.data

        return None
    

    # Hàm hiển thị ảnh đầu tiên sử dụng Django Unfold
    def first_image(self, obj):
        # Giả sử get_first_image_url_from_firebase là hàm lấy URL ảnh từ Firebase
        url = get_first_image_url_from_firebase(obj.name)
        if url:
            return url
            # return format_html(
            #     f'<a href="{url}" target="_blank">'
            #     f'<img src="{url}" width="70" height="70" style="border-radius: 50%; object-fit: cover; margin-right: 10px;" />'
            #     '</a>'
            # )

        return "No Image"
        # default_image_url = "/static/images/avatar.png"  # Đường dẫn đến ảnh mặc định trong thư mục static
        # return format_html(f'<img src="{default_image_url}" width="70" height="70" style="border-radius: 50%; object-fit: cover;" />')

    first_image.short_description = "First Image"  # Tiêu đề cho cột ảnh
    first_image.allow_tags = True  # Cho phép hiển thị HTML (nếu cần)

    def get_urls(self):
        return super().get_urls() + [
            path(
                "custom-url-path",
                MyStatistical.as_view(model_admin=self),
                name="custom_view",
            ),
            path(
                "store-url-path",
                MyStore.as_view(model_admin=self),
                name="store_view",
            ),
        ]
    
@register_component
class TrackerComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []

        for i in range(1, 72):
            has_value = random.choice([True, True, True, True, False])
            color = None
            tooltip = None
            if has_value:
                value = random.randint(2, 6)
                color = f"bg-primary-{value}00 dark:bg-primary-{9 - value}00"
                tooltip = f"Value {value}"

            data.append(
                {
                    "color": color,
                    "tooltip": tooltip,
                }
            )

        context["data"] = data
        return context

@register_component
class CohortComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = []
        headers = []
        cols = []

        dates = reversed(
            [(now() - timedelta(days=x)).strftime("%B %d, %Y") for x in range(8)]
        )
        groups = range(1, 10)

        for row_index, date in enumerate(dates):
            cols = []

            for col_index, _col in enumerate(groups):
                color_index = 8 - row_index - col_index
                col_classes = []

                if color_index > 0:
                    col_classes.append(
                        f"bg-primary-{color_index}00 dark:bg-primary-{9 - color_index}00"
                    )

                if color_index >= 4:
                    col_classes.append("text-white dark:text-gray-600")

                value = random.randint(
                    4000 - (col_index * row_index * 225),
                    5000 - (col_index * row_index * 225),
                )

                subtitle = f"{random.randint(10, 100)}%"

                if value <= 0:
                    value = 0
                    subtitle = None

                cols.append(
                    {
                        "value": value,
                        "color": " ".join(col_classes),
                        "subtitle": subtitle,
                    }
                )

            rows.append(
                {
                    "header": {
                        "title": date,
                        "subtitle": f"Total {sum(col['value'] for col in cols):,}",
                    },
                    "cols": cols,
                }
            )

        for index, group in enumerate(groups):
            total = sum(row["cols"][index]["value"] for row in rows)

            headers.append(
                {
                    "title": f"Group #{group}",
                    "subtitle": f"Total {total:,}",
                }
            )
        context["data"] = {
            "headers": headers,
            "rows": rows,
        }


class EmployeeAdmin(unfold_admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'age', 'salary')
    search_fields = ('first_name', 'last_name')  # Tìm kiếm theo tên (chú ý dấu phẩy để định nghĩa tuple)
    list_filter = ('first_name', 'last_name', 'gender', 'age', 'salary')

    list_filter = [
        FullNameFilter,
        GreaterSalaryFilter,
    ]
    list_filter_submit = True
    list_fullwidth = True

admin.site.register(Employee, EmployeeAdmin)

# Đăng ký model
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(User)  
admin.site.unregister(Group)  


admin.site.register(User, CustomUserAdmin)  
admin.site.register(Group, CustomGroupAdmin) 


# C:\Users\Admin\AppData\Roaming\Python\Python312\site-packages\django_google_sso\admin.py



