# Một dự án chưa có tên

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

**Step 6 .** Kích hoạt máy ảo

```bash
.\venv\Scripts\activate
```

**Step 7 .** Tạo file `requirements.txt` và file `Procfile `

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

**Step 8 .** Đảm bảo `settings.py` có chứa

- Giúp không bị mất `css`

  ```python
  import django_heroku
  django_heroku.settings(locals())
  ```

- Đảm bảo có chứa tên miền
  
  ```python
  ALLOWED_HOSTS = [
      'chat-123-b5f27fe98cab.herokuapp.com',
  ]
  ```

**Step 9 .** Tạo app trên `Heroku` tại [Heroku](https://dashboard.heroku.com/)


**Step 10 .** Đăng nhập `Heroku` bằng cách sử dụng câu lệnh sau trên `powershell` sau đó nhấn `Enter`

  ```
  heroku login
  ```

**Step 11 .** Tạo kho lưu trữ

```
git init
```

**Step 12 .** Tạo kho file `.gitignore`

```
touch .gitignore
```

- Nội dung file có

```
.env
venv/
```

**Step 13 .** Kết nối với `project-1233` tên app mà bạn đã đặt trên `Heroku`

```
heroku git:remote -a project-1233
```


```
git add .
```

```
git commit -am "make it better"
```

```
git push heroku master
```

**Step 14 .** Cài đặt thư viện
```
pip install -r requirements.txt
```

**Step 15 .** Chú ý lần này không đẩy file `db.sqlite3` lên `heroku` nữa mà kết nối `aiven.io`

1. Tài khoản `aiven.io` là bắt buộc, bạn có thể đăng ký tài khoản tại [aiven](https://console.aiven.io/)

2. Đảm bảo requirements.txt chứa các thư viện sau

```
Django==5.0.6
django-heroku==0.3.1
gunicorn==22.0.0
mysqlclient==2.2.4
python-dotenv==1.0.1
```

3. Cài lại các thư viện trên bằng

```
pip install -r requirements.txt
```

4. Đảm bảo chứa tên miền trong `setting.py`

```
ALLOWED_HOSTS = ['project-1233-6f93642d7963.herokuapp.com']
```

5. Đảm bảo có các dòng này trong `setting.py`

```
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

```
DB_ENGINE=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

8. Đẩy code lên `heroku` trừ `db.sqlite3`

```
git add .
```

```
git commit -m "connect aiven.io"
```

```
git push heroku master
```

8. Cấu hình `.env` trên `heroku`



### Project authentication and email

**Step 1 .** Tạo `authentication`

```
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
EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
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

```
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
  <img src="docs/images/django-google-sso.png" alt="Django Google SSO"/>
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

## Welcome to Django Google SSO

This library aims to simplify the process of authenticating users with Google in Django Admin pages,
inspired by libraries like [django_microsoft_auth](https://github.com/AngellusMortis/django_microsoft_auth)
and [django-admin-sso](https://github.com/matthiask/django-admin-sso/)

---

### Documentation

* Docs: https://megalus.github.io/django-google-sso/

---

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
# settings.py

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

<p align="center">
   <img src="docs/images/django_login_with_google_light.png"/>
</p>

---

## License

This project is licensed under the terms of the MIT license.