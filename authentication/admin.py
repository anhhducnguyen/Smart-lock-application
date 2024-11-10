from pyexpat.errors import messages
from django.contrib import admin
from django.contrib.auth.models import User, Group  
from unfold.admin import ModelAdmin
from django_google_sso.models import GoogleSSOUser
from django.templatetags.static import static
from unfold.decorators import action, display
from authentication.sites import formula_admin_site
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
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


class FullNameFilter(TextFilter):
    title = ("username")
    parameter_name = "username"

    def queryset(self, request, queryset):
        if self.value() in EMPTY_VALUES:
            return queryset

        return queryset.filter(
            Q(first_name__icontains=self.value()) | Q(last_name__icontains=self.value())
        )

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

@admin.register(Group, site=formula_admin_site)
class CustomGroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

   
class CustomGoogleSSOUserAdmin(ModelAdmin):
    list_display = ('user', 'google_id', 'picture_url', 'locale')
    search_fields = ('user__username', 'google_id', 'locale')
    fieldsets = (
        (None, {'fields': ('user', 'google_id', 'picture_url', 'locale')}),
    )

from django.contrib import admin
from .models import Status, UserProfile
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

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('name', 'first_image_url')  # Hiển thị tên và URL ảnh đầu tiên

#     # Hàm hiển thị ảnh đầu tiên
#     def first_image_url(self, obj):
#         url = get_first_image_url_from_firebase(obj.name)
#         if url:
#             return format_html(f'<img src="{url}" width="50" height="50" />')  # Hiển thị ảnh thumbnail
#         return "No Image"
    
#     first_image_url.short_description = "First Image"  # Tiêu đề cho cột ảnh

# from unfold import admin as unfold_admin
# class UserProfileAdmin(unfold_admin.ModelAdmin):
#     list_display = ('name', 'first_image')  # Hiển thị tên và ảnh đầu tiên
#     # search_fields = ('name')

#     # Hàm hiển thị ảnh đầu tiên sử dụng Django Unfold
#     def first_image(self, obj):
#         # Giả sử get_first_image_url_from_firebase là hàm lấy URL ảnh từ Firebase
#         url = get_first_image_url_from_firebase(obj.name)
#         if url:
#             # Trả về URL cho Unfold để hiển thị ảnh
#             return url
#         return "No Image"

#     first_image.short_description = "First Image"  # Tiêu đề cho cột ảnh

# # Đăng ký model
# admin.site.register(UserProfile, UserProfileAdmin)

from unfold import admin as unfold_admin
from django.utils.html import mark_safe

class UserProfileAdmin(unfold_admin.ModelAdmin):
    list_display = ('display_picture', 'name', 'age', 'sex', 'date_join', 'email', "display_status",)  # Hiển thị tên và ảnh đầu tiên
    # list_display = ('picture', 'name', 'age', 'sex', 'date_join', 'email', "display_status",)
    search_fields = ('name',)  # Tìm kiếm theo tên (chú ý dấu phẩy để định nghĩa tuple)
    list_filter = ('name', 'age', 'sex', 'date_join', 'email')

    search_fields = ('name', 'email',)

    list_filter = [
        FullNameFilter,
        ("data", ChoicesDropdownFilter),
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

# Đăng ký model
admin.site.register(UserProfile, UserProfileAdmin)



admin.site.unregister(User)  # Hủy đăng ký mặc định
admin.site.unregister(Group)  # Hủy đăng ký mặc định
# admin.site.unregister(GoogleSSOUser)
# admin.site.register(GoogleSSOUser)
# admin.site.unregister(UserProfile) 

admin.site.register(User, CustomUserAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
admin.site.register(Group, CustomGroupAdmin)  # Đăng ký với lớp quản trị tùy chỉnh
# admin.site.register(GoogleSSOUser, CustomGoogleSSOUserAdmin)



