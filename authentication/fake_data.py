from faker import Faker
import json
from datetime import datetime
import pytz  # Thêm thông tin múi giờ thủ công

fake = Faker()
users = []

# Múi giờ mặc định
timezone = pytz.timezone("Asia/Ho_Chi_Minh")  # Thay bằng múi giờ của bạn

for i in range(300):  # Tạo 300 người dùng mẫu
    date_joined_naive = fake.date_time_this_year()  # Tạo naive datetime
    date_joined_aware = timezone.localize(date_joined_naive)  # Chuyển thành aware datetime

    users.append({
        "model": "auth.user",
        "pk": i + 1,
        "fields": {
            "username": fake.user_name(),
            "password": fake.password(),
            "is_superuser": False,
            "is_staff": False,
            "is_active": True,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "date_joined": date_joined_aware.isoformat(),  # Ghi aware datetime
        }
    })

# Lưu file JSON
with open("authentication/fixtures/0003_user.json", "w") as f:
    json.dump(users, f, indent=4)
