# Smart lock application

[Link to website](https://project-1233-6f93642d7963.herokuapp.com/)

## Table of Contents

- [Installation](#installation)
- [Deployment](#deployment)
- [Send Email](#send-email)
- [Google SSO](#google-sso)
- [Firebase](#firebase)
- [Check](#check)

## Installation

**Step 1 .** Create a project named `project`

```bash
django-admin startproject project
```

**Step 2 .** Migrate the database data

```bash
python manage.py migrate
```

**Step 3 .** Launch the site test

```bash
python manage.py runserver
```

**Step 4 .** Create the virtual machine

```bash
python -m venv myenv
```

**Step 5 .** Create the virtual machine

```bash
python -m venv myenv
```

**Step 6 .** Create the `.env` file

```bash
touch .env
```

**Step 7 .** In the file `.env`

```bash
DB_ENGINE=django.db.backends.mysql
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port

GOOGLE_SSO_CLIENT_ID=your_google_sso_client_id
GOOGLE_SSO_PROJECT_ID=your_google_sso_project_id
GOOGLE_SSO_CLIENT_SECRET=your_google_sso_client_secret

LOGIN_USERNAME=your_login_username
LOGIN_PASSWORD=your_login_password
```

**Step 8 .** Activate the virtual machine

```bash
.\venv\Scripts\activate
```

**Step 9 .** Create file `requirements.txt` and file `Procfile `

- Create file `requirements.txt`

 ```bash
 touch requirements.txt
 ```

- Create file `Procfile`

 ```bash
 touchProfile
 ```


- Contents of file `requirements.txt`

 ```python
Django==5.0.6
django-heroku==0.3.1
gunicorn==22.0.0
```

- `Procfile` file contents

```python
web: gunicorn project.wsgi --log-file -
```

**Step 10 .** Make sure `settings.py` contains

- Helps avoid losing `css`

```python
import django_heroku
django_heroku.settings(locals())
```

- Make sure it contains the domain

``` python
ALLOWED_HOSTS = [
'project-1233-6f93642d7963.herokuapp.com',
'127.0.0.1',
'localhost',
]
```
**Step 11 .** Create dummy data into .json files

```bash
python authentication\fake_data\employees.py
python authentication\fake_data\users.py
```
**Step 12 .** Load data into models

```bash
python manage.py loaddata 0001_userprofile .json
python manage.py loaddata 0002_user.json
python manage.py loaddata 0003_employee.json
```

**Step 13 .** Run the program

```bash
python manage.py runserver
```

## Deployment

**Step 1 .** Create an app on `Heroku` at [Heroku](https://dashboard.heroku.com/)

**Step 2 .** Log in to `Heroku` by using the following command on `powershell` then press `Enter`

```
heroku login
```
**Step 3 .** Create a repository

```
git init
```
**Step 4 .** Create a repository file `.gitignore`

```
touch .gitignore
```

- The file content has

```
.env
venv/
```
**Step 5 .** Connect to `project-1233` the name of the app you set on `Heroku`

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

**Step 6 .** Install libraries

```bash
pip install -r requirements.txt
```

**Step 7 .** Note that this time do not push the `db.sqlite3` file to `heroku` but connect to `aiven.io`

1. An `aiven.io` account is required, you can register an account at [aiven](https://console.aiven.io/)

2. Make sure requirements.txt contains libraries after

```python
Django==5.0.6
django-heroku==0.3.1
gunicorn==22.0.0
mysqlclient==2.2.4
python-dotenv==1.0.1
```

3. Reinstall the above libraries using

```bash
pip install -r requirements.txt
```

4. Make sure to include the domain name in `setting.py`

```python
ALLOWED_HOSTS = ['project-1233-6f93642d7963.herokuapp.com']
```

5. Make sure to have these lines in `setting.py`

```python
import os
from pathlib import Path
from dotenv import load_dotenv
```

6. Make sure to have these lines in `setting.py` to get data from the file `.env`

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

7. Configure connection `aiven.io`

```python
DB_ENGINE=your_database_engine
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
```

8. Push the code to `heroku` except `db.sqlite3`

```bash
git add .
```

```bash
git commit -m "connect aiven.io"
```

```bash
git push heroku master
```

8. Configure `.env` on `heroku`

## Send Email

**Step 1 .** Create `authentication`

```bash
python manage.py startapp authentication
```
**Step 2 .** Make sure `setting.py` is added

```python
INSTALLED_APPS = [
'authentication',
]
```
**Step 3 .** Make sure `project/info.py` is added

```python
EMAIL_USE_TLS=True
EMAIL_HOST=your_email_host
EMAIL_HOST_USER=your_email_user
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_PORT=587
```
**Step 3 .** Make sure `project/urls.py` is added

```python
from django.urls import path, include. include

urlpatterns = [
 path('admin/', admin.site.urls),
 path('', include('authentication.urls'))
]
```

**Step 4 .** Make sure to add `project/wsgi.py`

```python
app = application
```

**Step 4 .** Make sure to add `authentication/token.py`

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

**Step 5 .** Create `authentication/urls.py`

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

**Step 5 .** Install the library

```bash
pip install six
```

**Step 6 .** Make sure this is there so it finds the templates folder `project/settings.py`

```python
TEMPLATES = [
{
'DIRS': ["templates"],
},
]
```
**Step 7 .** Configure gmail in `project/settings.py`

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
 "django.contrib.messages", # Need for Auth messages
 "django_google_sso", # Add django_google_sso
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


## Firebase

Step 1: First you need to go to the [firebase](https://firebase.google.com/) page, logging in to your account is required.

Step 2: Select `Go to console` in the upper right corner of the screen

Step 3: Select `Create a project` to create a new project, name the project and select `Continue`

Step 4: Select `Default Account for Firebase`, then select `Create project` wait and select `Continue`

Step 5: At `Project Overview` select `Storage`

[Video tutorial](https://www.youtube.com/watch?v=-IFRVMEhZDc)

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

Install additional packages

```bash
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt

touch Aptfile

libgl1-mesa-glx
```

```bash
python manage.py shell. shell
```


```python
from authentication.models import UserProfile
```

```python
profiles = UserProfile.objects.all()
for profiles in profiles:
 print(f"Name: {profile.name}")
 print(f"Picture: {profile.picture}")
 print(f"Age: {profile.age}")
 print(f"Sex: {profile.sex}")
 print(f"Date join: {profile.date_join}")
 print(f"Email: {profile.email}")
 print(f"Status: {profile.data}")
```

## License

This project is licensed under the terms of the MIT license.