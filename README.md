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



# Django Framework

## Giới thiệu

Django là một trong những framework web phổ biến nhất được xây dựng bằng Python, nổi tiếng với khả năng phát triển nhanh chóng và tập trung vào thiết kế sạch sẽ, dễ bảo trì. Django được tạo ra bởi các lập trình viên với mục tiêu giảm thiểu các công việc lặp đi lặp lại trong phát triển web, giúp bạn tập trung vào phát triển ứng dụng với chất lượng cao hơn mà không cần phải lo lắng quá nhiều về các chi tiết kỹ thuật như bảo mật hay tối ưu hóa hiệu suất.

## Tính năng nổi bật

Django được xây dựng với nhiều tính năng mạnh mẽ, giúp nó trở thành một lựa chọn lý tưởng cho cả các dự án nhỏ lẫn các ứng dụng quy mô lớn:

### 1. Kiến trúc MTV (Model-Template-View)
Django sử dụng mô hình kiến trúc MTV (Model-Template-View), tương tự với MVC (Model-View-Controller), giúp phân tách rõ ràng các thành phần của ứng dụng web. Điều này không chỉ giúp mã nguồn dễ quản lý, mà còn hỗ trợ bảo trì và mở rộng ứng dụng một cách linh hoạt.

### 2. ORM (Object-Relational Mapping)
Một trong những tính năng nổi bật của Django là ORM mạnh mẽ, giúp bạn tương tác với cơ sở dữ liệu thông qua các mô hình Python mà không cần viết câu lệnh SQL trực tiếp. ORM của Django hỗ trợ nhiều hệ quản trị cơ sở dữ liệu như PostgreSQL, MySQL, SQLite và Oracle, cho phép bạn dễ dàng chuyển đổi giữa các hệ quản trị cơ sở dữ liệu mà không phải sửa đổi mã nguồn.

### 3. Giao diện quản trị tự động (Admin Interface)
Django đi kèm với một trang quản trị tự động, cung cấp đầy đủ các chức năng để quản lý và thao tác dữ liệu mà không cần phải phát triển từ đầu. Giao diện này có khả năng tùy biến cao và có thể mở rộng theo nhu cầu của ứng dụng, giúp tiết kiệm thời gian và công sức cho các tác vụ quản lý dữ liệu.

### 4. Hệ thống xác thực và phân quyền
Django cung cấp một hệ thống xác thực và phân quyền mạnh mẽ, bao gồm các tính năng như đăng ký, đăng nhập, thay đổi mật khẩu, và phân quyền cho người dùng. Hệ thống này dễ dàng tích hợp và mở rộng, đáp ứng nhu cầu bảo mật của các ứng dụng web hiện đại.

### 5. Bảo mật hàng đầu
Bảo mật là một trong những ưu tiên hàng đầu của Django. Framework này được thiết kế để bảo vệ ứng dụng của bạn khỏi các lỗ hổng bảo mật phổ biến như SQL Injection, XSS (Cross-Site Scripting), CSRF (Cross-Site Request Forgery), và nhiều hình thức tấn công khác. Django cũng liên tục cập nhật các bản vá bảo mật để đảm bảo rằng ứng dụng của bạn luôn được bảo vệ trước các mối đe dọa mới.

### 6. Khả năng mở rộng và tích hợp
Django rất linh hoạt, cho phép bạn mở rộng và tùy chỉnh ứng dụng của mình một cách dễ dàng. Framework này hỗ trợ việc xây dựng các ứng dụng nhỏ gọn (apps) có thể tái sử dụng và dễ dàng tích hợp với các hệ thống khác thông qua REST API hoặc GraphQL.

### 7. Cộng đồng và tài liệu phong phú
Django có một cộng đồng phát triển lớn và tích cực, luôn sẵn sàng hỗ trợ bạn trong quá trình phát triển. Ngoài ra, Django đi kèm với tài liệu phong phú, chi tiết và dễ hiểu, giúp bạn dễ dàng tiếp cận và giải quyết các vấn đề phát sinh trong quá trình làm việc.

## Cài đặt Django

Django có thể được cài đặt dễ dàng bằng công cụ quản lý gói `pip`. Bạn chỉ cần chạy lệnh sau trong môi trường ảo Python:

```bash
pip install django
```

## Để xác nhận Django đã được cài đặt thành công, bạn có thể kiểm tra phiên bản bằng lệnh

```bash
python -m django --version
```

## Để khởi tạo một dự án mới trong Django, bạn có thể sử dụng lệnh `django-admin` như sau

```bash
django-admin startproject myproject
cd myproject
python manage.py runserver
```

[Django Official Documentation](https://docs.djangoproject.com/en/5.1/)

