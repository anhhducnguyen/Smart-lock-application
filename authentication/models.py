from django.utils import timezone
from django.db import models
from firebase_admin import storage
import os
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from django.db.models.signals import post_delete
from django.dispatch import receiver

class Status(models.TextChoices):
    ACTIVE = "ACTIVE", ("Active")
    INACTIVE = "INACTIVE", ("Inactive")

from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    age = models.PositiveIntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    name = models.CharField(max_length=100, unique=True)
    picture = models.ImageField("picture", null=True, blank=True, default=None)
    age = models.IntegerField(default=18)
    sex = models.CharField(max_length=10, default="Male")
    # status = models.CharField(max_length=100, default="Active")
    date_join = models.DateField(default=timezone.now)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    deleted_folders = models.TextField(null=True, blank=True)  # Lưu trữ tên các thư mục đã xóa
    data = models.CharField(
        ("status"), choices=Status.choices, null=True, blank=True, max_length=255
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Kiểm tra nếu tên thay đổi để xóa ảnh cũ trên Firebase
        if self.pk:
            old_instance = UserProfile.objects.get(pk=self.pk)
            if old_instance.name != self.name and old_instance.picture:
                old_folder_path = f"images/{old_instance.name}/"
                extension = os.path.splitext(old_instance.picture.path)[-1]
                bucket = storage.bucket()
                blob = bucket.blob(f"{old_folder_path}0{extension}")
                try:
                    blob.delete()
                    print(f"Đã xóa ảnh cũ trên Firebase tại {old_folder_path}0{extension}")
                except Exception as e:
                    print(f"Lỗi khi xóa ảnh cũ trên Firebase: {e}")

        # Nếu đây là lần lưu đầu tiên và có ảnh trong trường picture
        if not self.pk and self.picture:
            try:
                response = requests.get(self.picture.url, stream=True)
                if response.status_code == 200:
                    temp_file = NamedTemporaryFile(delete=True)
                    temp_file.write(response.content)
                    temp_file.flush()

                    file_name = os.path.basename(self.picture.url)
                    self.picture.save(file_name, File(temp_file), save=False)
                    print(f"Ảnh đã được lưu vào thư mục media: {self.picture.path}")
                else:
                    print("Không thể tải ảnh từ link được cung cấp.")
            except Exception as e:
                print(f"Lỗi khi tải ảnh: {e}")

        super().save(*args, **kwargs)

        # Đẩy ảnh lên Firebase với tên mới
        if self.picture:
            folder_path = f"images/{self.name}/"
            extension = os.path.splitext(self.picture.path)[-1]
            bucket = storage.bucket()
            blob = bucket.blob(f"{folder_path}0{extension}")

            try:
                blob.upload_from_filename(self.picture.path)
                print(f"Ảnh đã được tải lên Firebase tại {folder_path}0{extension}")
            except Exception as e:
                print(f"Lỗi khi đẩy ảnh lên Firebase: {e}")

    # def save(self, *args, **kwargs):
    #     if not self.pk and self.picture:
    #         # Nếu có link ảnh, tải ảnh về và lưu vào thư mục media
    #         try:
    #             response = requests.get(self.picture.url, stream=True)
    #             if response.status_code == 200:
    #                 # Tạo tệp tạm thời để lưu ảnh
    #                 temp_file = NamedTemporaryFile(delete=True)
    #                 temp_file.write(response.content)
    #                 temp_file.flush()
                    
    #                 # Lưu ảnh vào trường picture
    #                 file_name = os.path.basename(self.picture.url)
    #                 self.picture.save(file_name, File(temp_file), save=False)
    #                 print(f"Ảnh đã được lưu vào thư mục media: {self.picture.path}")
    #             else:
    #                 print("Không thể tải ảnh từ link được cung cấp.")
    #         except Exception as e:
    #             print(f"Lỗi khi tải ảnh: {e}")
        
    #     # Tiếp tục với phương thức lưu như cũ
    #     super().save(*args, **kwargs)
        
    #     # Đẩy ảnh lên Firebase với tên là "0.<định dạng ảnh>"
    #     if self.picture:
    #         folder_path = f"images/{self.name}/"
    #         extension = os.path.splitext(self.picture.path)[-1]  # Lấy định dạng ảnh từ đường dẫn
    #         bucket = storage.bucket()
    #         blob = bucket.blob(f"{folder_path}0{extension}")  # Đặt tên ảnh là "0.<định dạng>"

    #         try:
    #             blob.upload_from_filename(self.picture.path)
    #             print(f"Ảnh đã được tải lên Firebase tại {folder_path}0{extension}")
    #         except Exception as e:
    #             print(f"Lỗi khi đẩy ảnh lên Firebase: {e}")
    
    # Tín hiệu để xóa ảnh trên Firebase khi xóa UserProfile
@receiver(post_delete, sender=UserProfile)
def delete_picture_on_firebase(sender, instance, **kwargs):
    if instance.picture:
        folder_path = f"images/{instance.name}/"
        extension = os.path.splitext(instance.picture.path)[-1]
        bucket = storage.bucket()
        blob = bucket.blob(f"{folder_path}0{extension}")

        try:
            blob.delete()
            print(f"Ảnh đã được xóa khỏi Firebase tại {folder_path}0{extension}")
        except Exception as e:
            print(f"Lỗi khi xóa ảnh trên Firebase: {e}")




# from authentication.models import UserProfile


# profiles = UserProfile.objects.all()
# for profile in profiles:
#     print(f"Name: {profile.name}")
#     print(f"Picture: {profile.picture}")
#     print(f"Age: {profile.age}")
#     print(f"Sex: {profile.sex}")
#     print(f"Date join: {profile.date_join}")
#     print(f"Email: {profile.email}")
#     print(f"Status: {profile.data}")
#     print("------------")
