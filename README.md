# Smart lock application

[Liên kết đến trang web](https://project-1233-6f93642d7963.herokuapp.com/)

## Table of Contents

- [Installation](#installation)
- [Deployment](#deployment)
- [Send Email](#send-email)
- [Google SSO](#google-sso)
- [Firebase](#firebase)
- [Check](#check)
- [Django Framework](#django-framework)
- [Security in Django](#security-in-django)
- [License](#license)



## Installation

**Step 1 .** Tạo dự án có tên `project`

```bash
django-admin startproject project
```

**Step 2 .** Di chuyển cơ sở dữ liệu

```bash
python manage.py migrate
```

**Step 3 .** Khởi chạy kiểm tra trang web

```bash
python manage.py runserver
```

**Step 4 .** Tạo máy ảo

```bash
python -m venv myenv
```

**Step 5 .** Tạo máy ảo

```bash
python -m venv myenv
```

**Step 6 .** Tạo file `.env`

```bash
touch .env
```

**Step 7 .** Trong file `.env`

```bash
DB_ENGINE=django.db.backends.mysql
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
```

**Step 8 .** Kích hoạt máy ảo

```bash
.\venv\Scripts\activate
```

**Step 9 .** Tạo file `requirements.txt` và file `Procfile `

- Tạo file `requirements.txt`

    ```bash
    touch requirements.txt
    ```

- Tạo file `Procfile`

    ```bash
    touch Procfile
    ```


- Nội dung file `requirements.txt`

    ```python
    Django==5.0.6
    django-heroku==0.3.1
    gunicorn==22.0.0
    ```

- Nội dung file `Procfile`

    ```python
    web: gunicorn project.wsgi --log-file -
    ```

**Step 10 .** Đảm bảo `settings.py` có chứa

- Giúp không bị mất `css`

  ```python
  import django_heroku
  django_heroku.settings(locals())
  ```

- Đảm bảo có chứa tên miền
  
  ```python
    ALLOWED_HOSTS = [
        'project-1233-6f93642d7963.herokuapp.com',
        '127.0.0.1',
        'localhost',
    ]
  ```
**Step 11 .** Tạo dữ liệu giả vào các file .json

```bash
python authentication\fake_data\employees.py
python authentication\fake_data\users.py
```

**Step 12 .** Nạp dữ liệu cho models

```bash
python manage.py loaddata 0001_userprofile.json
python manage.py loaddata 0002_user.json
python manage.py loaddata 0003_employee.json
```

**Step 13 .** Chạy chương trình

```bash
python manage.py runserver
```

## Deployment

**Step 1 .** Tạo app trên `Heroku` tại [Heroku](https://dashboard.heroku.com/)


**Step 2 .** Đăng nhập `Heroku` bằng cách sử dụng câu lệnh sau trên `powershell` sau đó nhấn `Enter`

  ```
  heroku login
  ```

**Step 3 .** Tạo kho lưu trữ

```
git init
```

**Step 4 .** Tạo kho file `.gitignore`

```
touch .gitignore
```

- Nội dung file có

```
.env
venv/
```

**Step 5 .** Kết nối với `project-1233` tên app mà bạn đã đặt trên `Heroku`

```bash
heroku git:remote -a project-1233
```


```bash
git add .
```

```bash
git commit -am "make it better"
```

```bash
git push heroku master
```

**Step 6 .** Cài đặt thư viện

```bash
pip install -r requirements.txt
```

**Step 7 .** Chú ý lần này không đẩy file `db.sqlite3` lên `heroku` nữa mà kết nối `aiven.io`

1. Tài khoản `aiven.io` là bắt buộc, bạn có thể đăng ký tài khoản tại [aiven](https://console.aiven.io/)

2. Đảm bảo requirements.txt chứa các thư viện sau

```python
Django==5.0.6
django-heroku==0.3.1
gunicorn==22.0.0
mysqlclient==2.2.4
python-dotenv==1.0.1
```

3. Cài lại các thư viện trên bằng

```bash
pip install -r requirements.txt
```

4. Đảm bảo chứa tên miền trong `setting.py`

```python
ALLOWED_HOSTS = ['project-1233-6f93642d7963.herokuapp.com']
```

5. Đảm bảo có các dòng này trong `setting.py`

```python
import os
from pathlib import Path
from dotenv import load_dotenv
```

6. Đảm bảo có các dòng này trong `setting.py` để lấy dữ liệu từ file `.env`

```python
load_dotenv()

DATABASES = {
    "default": {
        "ENGINE": os.getenv('DB_ENGINE'),
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('DB_USER'),
        "PASSWORD": os.getenv('DB_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT'),
    }
}   
```

7. Cấu hình kết nối `aiven.io`

```python
DB_ENGINE=your_database_engine
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
```

8. Đẩy code lên `heroku` trừ `db.sqlite3`

```bash
git add .
```

```bash
git commit -m "connect aiven.io"
```

```bash
git push heroku master
```

8. Cấu hình `.env` trên `heroku`



## Send Email

**Step 1 .** Tạo `authentication`

```bash
python manage.py startapp authentication
```

**Step 2 .** Đảm bảo đã thêm vào `setting.py`

```python
INSTALLED_APPS = [
        'authentication',
]
```

**Step 3 .** Đảm bảo đã thêm vào `project/info.py`

```python
EMAIL_USE_TLS=True
EMAIL_HOST=your_email_host
EMAIL_HOST_USER=your_email_user
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_PORT=587
```

**Step 3 .** Đảm bảo đã thêm vào `project/urls.py`

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls'))
]
```

**Step 4 .** Đảm bảo đã thêm vào `project/wsgi.py`

```python
app = application
```

**Step 4 .** Đảm bảo đã thêm vào `authentication/token.py`

```python
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (
        text_type(user.pk) + text_type(timestamp) 
        # text_type(user.profile.signup_confirmation)
        )

generate_token = TokenGenerator()
```

**Step 5 .** Tạo `authentication/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
]
```

**Step 5 .** Cài đặt thư viện

```bash
pip install six
```

**Step 6 .** Đảm bảo có đoạn này để nó tìm được thư mục templates `project/settings.py`

```python
TEMPLATES = [
    {
        'DIRS': ["templates"],
    },
]
```

**Step 7 .** Cấu hình gmail trong `project/settings.py`

```python
from . info import *

EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT
```


<p align="center">
  <img src="https://github.com/megalus/django-google-sso/blob/main/docs/images/django-google-sso.png" alt="Django Google SSO"/>
</p>
<p align="center">
<em>Easily integrate Google Authentication into your Django projects</em>
</p>

<p align="center">
<a href="https://pypi.org/project/django-google-sso/" target="_blank">
<img alt="PyPI" src="https://img.shields.io/pypi/v/django-google-sso"/></a>
<a href="https://github.com/megalus/django-google-sso/actions" target="_blank">
<img alt="Build" src="https://github.com/megalus/django-google-sso/workflows/tests/badge.svg"/>
</a>
<a href="https://www.python.org" target="_blank">
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/django-google-sso"/>
</a>
<a href="https://www.djangoproject.com/" target="_blank">
<img alt="PyPI - Django Version" src="https://img.shields.io/pypi/djversions/django-google-sso"/>
</a>
</p>

## Google SSO

This library aims to simplify the process of authenticating users with Google in Django Admin pages,
inspired by libraries like [django_microsoft_auth](https://github.com/AngellusMortis/django_microsoft_auth)
and [django-admin-sso](https://github.com/matthiask/django-admin-sso/)



### Documentation

* Docs: https://megalus.github.io/django-google-sso/

### Install

```shell
$ pip install django-google-sso
```

### Configure

1. Add the following to your `settings.py` `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
    # other django apps
    "django.contrib.messages",  # Need for Auth messages
    "django_google_sso",  # Add django_google_sso
]
```

2. In [Google Console](https://console.cloud.google.com/apis/credentials) at _Api -> Credentials_, retrieve your
   Project Credentials and add them in your `settings.py`:

```python
GOOGLE_SSO_CLIENT_ID = "your client id here"
GOOGLE_SSO_PROJECT_ID = "your project id here"
GOOGLE_SSO_CLIENT_SECRET = "your client secret here"
```

3. Add the callback uri `http://localhost:8000/google_sso/callback/` in your Google Console, on the "Authorized Redirect
   URL".

4. Let Django Google SSO auto create users for allowable domains:

```python
# settings.py

GOOGLE_SSO_ALLOWABLE_DOMAINS = ["example.com"]
```

5. In `urls.py` please add the **Django-Google-SSO** views:

```python
# urls.py

from django.urls import include, path

urlpatterns = [
    # other urlpatterns...
    path(
        "google_sso/", include("django_google_sso.urls", namespace="django_google_sso")
    ),
]
```

6. And run migrations:

```shell
$ python manage.py migrate
```

That's it. Start django on port 8000 and open your browser in `http://localhost:8000/admin/login` and you should see the
Google SSO button.

---

## Firebase

Step 1: Đầu tiên bạn cần vào trang [firebase](https://firebase.google.com/), đăng nhập tài khoản là bắt buộc.

Step 2: Chọn `Go to console` ở góc trên phía bên phải màn hình

Step 3: Chọn `Create a project` để tạo dự án mới, đặt tên cho dự án và chọn `Continue` 

Step 4: Chọn `Default Account for Firebase`, rồi chọn `Create project` chờ và chọn `Continue`

Step 5: Tại `Project Overview` chọn `Storage` 

[Video hướng dẫn](https://www.youtube.com/watch?v=-IFRVMEhZDc)



## Check

```shell
heroku run python manage.py shell --app project-1233
```

```python
from django.apps import apps

auth_models = apps.get_app_config('auth').get_models()
for model in auth_models:
    print(model)

```

```python
from django.apps import apps

for app in apps.get_app_configs():
    for model in app.get_models():
        if model.__name__ == 'GoogleSSOUser':
            print(f"Found GoogleSSOUser in app: {app.name}")
            print(model)
```

```shell
heroku run python manage.py migrate --app project-1233
```

```shell
heroku run python manage.py makemigrations --app chat-123
```

```shell
heroku run python manage.py shell --app project-1233
```

Cài thêm package

```bash
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt

touch Aptfile

libgl1-mesa-glx
```

```bash
python manage.py shell
```


```python
from authentication.models import UserProfile
```

```python
profiles = UserProfile.objects.all()
for profile in profiles:
    print(f"Name: {profile.name}")
    print(f"Picture: {profile.picture}")
    print(f"Age: {profile.age}")
    print(f"Sex: {profile.sex}")
    print(f"Date join: {profile.date_join}")
    print(f"Email: {profile.email}")
    print(f"Status: {profile.data}")
    print("------------")
```

## License

This project is licensed under the terms of the MIT license.
