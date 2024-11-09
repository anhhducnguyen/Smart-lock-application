# from django.db import models

# # django-unfold==0.29.1
    
# from firebase_admin import storage
# from django.db import models

# class UserProfile(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     picture = models.ImageField(("picture"), null=True, blank=True, default=None)

#     def __str__(self):
#         return self.name
    
#     def delete_images_from_firebase(folder_path):
#         bucket = storage.bucket()
#         blobs = bucket.list_blobs(prefix=folder_path)  # Lấy tất cả blobs bắt đầu với folder_path

#         # Xóa từng blob trong thư mục
#         for blob in blobs:
#             blob.delete()
#             print(f"Đã xóa file {blob.name} thành công.")

#     def delete(self, *args, **kwargs):
#         # Gọi hàm xóa ảnh từ Firebase trước khi xóa người dùng
#         # self.delete_images_from_firebase()
#         self.delete_images_from_firebase("images/test/")
#         super().delete(*args, **kwargs)

# from django.utils import timezone
# from django.db import models
# from firebase_admin import storage

# class UserProfile(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     picture = models.ImageField("picture", null=True, blank=True, default=None)
#     age = models.IntegerField(default=18)  # Thay CharField thành IntegerField cho trường 'age' nếu nó là tuổi
#     sex = models.CharField(max_length=10, default="Male")  # Giả sử "Male" là giá trị mặc định
#     status = models.CharField(max_length=100, default="Active")  # Giả sử "Active" là trạng thái mặc định
#     date_join = models.DateField(default=timezone.now)  # Ngày tham gia, mặc định là ngày hiện tại
#     email = models.EmailField(max_length=100, unique=True, null=True, blank=True)

#     def __str__(self):
#         return self.name
    
#     def delete_images_from_firebase(self, folder_path):
#         bucket = storage.bucket()
#         blobs = bucket.list_blobs(prefix=folder_path)

#         for blob in blobs:
#             blob.delete()
#             print(f"Đã xóa file {blob.name} thành công.")

#     def delete_folder_from_firebase(self, folder_path):
#         bucket = storage.bucket()
#         print(f"Bucket: {bucket.name}")  # In ra tên bucket để kiểm tra kết nối
#         blobs = bucket.list_blobs(prefix=folder_path)

#         for blob in blobs:
#             blob.delete()
#             print(f"Đã xóa file {blob.name} thành công.")


#     def delete(self, *args, **kwargs):
#         # Xóa thư mục dựa trên tên của người dùng
#         folder_path = f"images/{self.name}/"
#         self.delete_folder_from_firebase(folder_path)
#         super().delete(*args, **kwargs)

# from django.utils import timezone
# from django.db import models
# from firebase_admin import storage

# class UserProfile(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     picture = models.ImageField("picture", null=True, blank=True, default=None)
#     age = models.IntegerField(default=18)  # Tuổi mặc định là 18
#     sex = models.CharField(max_length=10, default="Male")  # Giả sử "Male" là giá trị mặc định
#     status = models.CharField(max_length=100, default="Active")  # Trạng thái mặc định là "Active"
#     date_join = models.DateField(default=timezone.now)  # Ngày tham gia mặc định là ngày hiện tại
#     email = models.EmailField(max_length=100, unique=True, null=True, blank=True)

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         # Kiểm tra nếu là đối tượng mới
#         if not self.pk:
#             # Tạo thư mục trên Firebase nếu chưa tồn tại
#             folder_path = f"images/{self.name}/"
#             bucket = storage.bucket()

#             try:
#                 # Kiểm tra nếu thư mục đã tồn tại
#                 blob = bucket.blob(folder_path)
#                 if not blob.exists():
#                     # Tạo thư mục trống bằng cách tải lên một file rỗng
#                     empty_blob = bucket.blob(f"{folder_path}placeholder.txt")
#                     empty_blob.upload_from_string("", content_type="text/plain")
#                     print(f"Đã tạo thư mục {folder_path} trên Firebase.")
#             except Exception as e:
#                 print(f"Lỗi khi kết nối tới Firebase hoặc tạo thư mục: {e}")

#         # Lưu đối tượng `UserProfile`
#         super().save(*args, **kwargs)

from django.utils import timezone
from django.db import models
from firebase_admin import storage

class Status(models.TextChoices):
    ACTIVE = "ACTIVE", ("Active")
    INACTIVE = "INACTIVE", ("Inactive")

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
        if not self.pk:
            # Tạo thư mục trên Firebase nếu chưa tồn tại
            folder_path = f"images/{self.name}/"
            bucket = storage.bucket()

            try:
                blob = bucket.blob(folder_path)
                if not blob.exists():
                    empty_blob = bucket.blob(f"{folder_path}placeholder.txt")
                    empty_blob.upload_from_string("", content_type="text/plain")
                    print(f"Đã tạo thư mục {folder_path} trên Firebase.")
            except Exception as e:
                print(f"Lỗi khi kết nối tới Firebase hoặc tạo thư mục: {e}")
        
        super().save(*args, **kwargs)

    def delete_folder_from_firebase(self):
        """Xóa tất cả các blobs trong thư mục của người dùng trên Firebase theo tên và lưu tên thư mục đã xóa"""
        folder_path = f"images/{self.name}/"  # Lấy thư mục theo tên người dùng
        bucket = storage.bucket()
        blobs = bucket.list_blobs(prefix=folder_path)

        deleted_files = []

        # Xóa từng blob trong thư mục
        for blob in blobs:
            try:
                blob.delete()
                deleted_files.append(blob.name)
                print(f"Đã xóa file {blob.name} thành công.")
            except Exception as e:
                print(f"Lỗi khi xóa file {blob.name}: {e}")

        # Lưu lại tên các thư mục đã xóa vào trường `deleted_folders`
        if deleted_files:
            deleted_folders = "\n".join(deleted_files)
            self.deleted_folders = deleted_folders
            self.save()  # Lưu lại thông tin vào cơ sở dữ liệu

        return deleted_files
