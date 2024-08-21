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


## Cấu trúc thư mục cơ bản

```python 

myproject/
    manage.py
    myproject/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
    app_name/
        migrations/
        __init__.py
        admin.py
        apps.py
        models.py
        tests.py
        views.py
```

### Trong đó:

**manage.py:** Tập lệnh dùng để quản lý các tác vụ liên quan đến dự án như chạy server, di chuyển cơ sở dữ liệu, và nhiều hơn nữa.

**settings.py:** File cấu hình chính của dự án, nơi bạn thiết lập các tùy chọn như cơ sở dữ liệu, ứng dụng cài đặt, bảo mật, và các thông số khác.

**urls.py:** File định tuyến, nơi bạn cấu hình các URL của ứng dụng và chỉ định view tương ứng.

**models.py:** Nơi bạn định nghĩa các mô hình dữ liệu (Models) cho ứng dụng của mình.

**views.py:** Nơi bạn định nghĩa các hàm xử lý logic ứng dụng và trả về phản hồi cho người dùng.


# Security in Django

## Potential Risks

1. **SQL Injection Vulnerabilities**:
   SQL Injection xảy ra khi một ứng dụng web cho phép người dùng nhập dữ liệu vào các truy vấn SQL một cách không an toàn, dẫn đến khả năng thực thi các lệnh SQL độc hại.

2. **Cross-Site Scripting (XSS)**:
   XSS xảy ra khi một ứng dụng cho phép người dùng nhập dữ liệu có thể chứa mã JavaScript độc hại, sau đó hiển thị lại cho người dùng khác mà không kiểm tra hoặc mã hóa.

3. **Cross-Site Request Forgery (CSRF)**:
   CSRF xảy ra khi người dùng không biết họ đang gửi một yêu cầu độc hại đến một ứng dụng web mà họ đã xác thực, dẫn đến việc thực hiện các hành động không mong muốn.

4. **Insecure Direct Object References (IDOR)**:
   IDOR xảy ra khi một ứng dụng cho phép truy cập trực tiếp vào các đối tượng dựa trên dữ liệu đầu vào của người dùng mà không kiểm tra quyền truy cập, dẫn đến việc lộ thông tin hoặc dữ liệu của người dùng khác.

5. **Broken Authentication and Session Management**:
   Vấn đề này xảy ra khi cơ chế xác thực và quản lý phiên không được cấu hình hoặc triển khai đúng cách, dẫn đến nguy cơ tấn công từ việc đoán mật khẩu, đánh cắp phiên, hoặc chiếm đoạt tài khoản.

6. **Security Misconfiguration**:
   Cấu hình bảo mật không chính xác xảy ra khi hệ thống hoặc ứng dụng không được cấu hình bảo mật đúng cách, dẫn đến các lỗ hổng bảo mật.

7. **Sensitive Data Exposure**:
   Lộ thông tin nhạy cảm xảy ra khi thông tin như mật khẩu, thông tin thẻ tín dụng, hoặc dữ liệu cá nhân không được bảo vệ đúng cách.

8. **Using Components with Known Vulnerabilities**:
   Sử dụng các thư viện, mô-đun hoặc phần mềm có các lỗ hổng bảo mật đã biết mà chưa được vá.

9. **Insufficient Logging and Monitoring**:
   Không ghi đầy đủ hoặc giám sát hoạt động của hệ thống, dẫn đến việc không phát hiện kịp thời các hành vi bất thường hoặc tấn công.

10. **File Upload Vulnerabilities**:
    Lỗ hổng liên quan đến việc tải lên tệp mà không kiểm tra đúng cách, có thể dẫn đến việc thực thi mã độc hoặc lộ thông tin.

11. **500 Internal Server Error**:
    Lỗi 500 xảy ra khi máy chủ gặp vấn đề không rõ và không thể xử lý yêu cầu.

12. **Key Exposure or Rubbish Characters**:
    Tiết lộ thông tin nhạy cảm như API keys, khóa mã hóa hoặc các ký tự không mong muốn xuất hiện trong dữ liệu.

## How to Mitigate These Risks

1. **SQL Injection**:
   - Sử dụng Django ORM: Django cung cấp ORM để xây dựng các truy vấn an toàn.

   ```python
   users = User.objects.filter(email=email)
   ```

   - Tránh viết các truy vấn SQL thô mà không có biện pháp bảo vệ.

2. **Cross-Site Scripting (XSS)**:
    - Sử dụng Django template engine: Django tự động mã hóa các biến trong template.

    ```python
    <h1>{{ user.name }}</h1>
    ```

    - Mã hóa đầu ra khi cần thiết: Sử dụng `django.utils.html.escape()` để mã hóa đầu ra.

3. **Cross-Site Request Forgery (CSRF)**:
    - Sử dụng CSRF tokens: Django tự động bảo vệ chống lại CSRF thông qua các token.

    - Kiểm tra CSRF token trong các yêu cầu quan trọng: Django xử lý điều này thông qua middleware CSRF.

4. **Insecure Direct Object References (IDOR)**:
    - Sử dụng middleware và decorators: Django cung cấp middleware và decorators để kiểm soát quyền truy cập vào tài nguyên.
    
    ```python
    @login_required
    def my_view(request, id):
        if request.user.id != id:
            return redirect('home')
    ```

    - Kiểm tra quyền sở hữu trước khi truy cập dữ liệu.

5. **Broken Authentication and Session Management**:

    - Sử dụng hệ thống xác thực tích hợp của Django: Django cung cấp cơ chế xác thực mạnh mẽ và dễ sử dụng.

    ```python 
    @login_required
    def profile_view(request):
        return render(request, 'profile.html')
    ```
    
    - Sử dụng HTTPS để bảo vệ thông tin đăng nhập và các phiên.
    - Cấu hình thời gian hết hạn phiên hợp lý trong `settings.py`:

6. **Security Misconfiguration**:

    - Kiểm tra và cấu hình đúng các tệp `.env`: Đảm bảo thông tin nhạy cảm không bị lộ.
    - Đặt `DEBUG=False` trong môi trường sản xuất để tránh lộ thông tin lỗi chi tiết.
    - Cấu hình quyền truy cập tệp và thư mục đúng cách.

7. **Sensitive Data Exposure**:

    - Sử dụng cơ chế mã hóa của Django: Django cung cấp phương thức mã hóa dữ liệu.

    ```python
    from django.core.exceptions import ImproperlyConfigured
    from django.conf import settings
    from cryptography.fernet import Fernet

    def encrypt_data(data):
        fernet = Fernet(settings.ENCRYPTION_KEY)
        return fernet.encrypt(data.encode())

    def decrypt_data(data):
        fernet = Fernet(settings.ENCRYPTION_KEY)
        return fernet.decrypt(data).decode()
    ```

    - Không lưu trữ thông tin nhạy cảm dưới dạng plain text: Sử dụng hàm `hash` để lưu trữ mật khẩu.
    - Sử dụng `HTTPS` để bảo vệ dữ liệu trong quá trình truyền tải.

8. **Using Components with Known Vulnerabilities**:

    - Thường xuyên cập nhật thư viện và `dependencies`: Sử dụng `pip` để cập nhật thư viện.

    ```python
    pip install --upgrade -r requirements.txt
    ```

    - Sử dụng các công cụ kiểm tra lỗ hổng như `Snyk` hoặc `OWASP Dependency-Check`.







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

# Duyệt qua tất cả các ứng dụng đã cài đặt trong dự án
for app in apps.get_app_configs():
    # Duyệt qua tất cả các model trong mỗi ứng dụng
    for model in app.get_models():
        # Kiểm tra nếu tên model là GoogleSSOUser
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


