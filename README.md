# DL91_event_management
DL91_event_management

- Create repo in GitHub and copy the repo link
- go to the specific location in your local system and open cmd
- check git is installed or not
>>> git --version
git version 2.41.0.windows.1

- clone your repo
>>> git clone https://github.com/brijeshpytops/DL91_event_management.git

- change your dir anf go to the project dir
>>> cd DL91_event_management

- this is your base dir
.../DL91_event_management >>>

- create virtual environment
.../DL91_event_management >>> python -m venv [your-env-name]

- add .gitignore file in "/[your-env-name]"

- Activate/Deactivate your virtual environment
.../DL91_event_management >>> [your-env-name]\Scripts\activate - for activate
([your-env-name]).../DL91_event_management >>> [your-env-name]\Scripts\deactivate - for deactivate

- create requirements.txt inside your base dir
([your-env-name]).../DL91_event_management >>> type nul > requirements.txt - for create file in windows os

- Now, check you have installed python in your local system or not 
- required python version for django [Python 3.x.y]
([your-env-name]).../DL91_event_management >>> python --version
Python 3.12.2

- Now install django and make sure you are in virtual env.
([your-env-name]).../DL91_event_management >>> pip install django

- Check django
([your-env-name]).../DL91_event_management >>> python
Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> django.get_version()
'5.1.4'

OR

([your-env-name]).../DL91_event_management >>> python -m django --version
5.1.4

- check all installed moduels and packages in your virtual env.
([your-env-name]).../DL91_event_management >>> pip list/pip freeze
Package  Version
-------- -------
asgiref  3.8.1
Django   5.1.4
pip      24.3.1
sqlparse 0.5.3
tzdata   2024.2

- add your installed modules and packages in your requirements.txt file when you install new modules and packages
([your-env-name]).../DL91_event_management >>> pip freeze > requirements.txt

- install modules and packages from requirements.txt
([your-env-name]).../DL91_event_management >>> pip install -r requirements.txt

- Now, Creating a project
([your-env-name]).../DL91_event_management >>> django-admin startproject [your-project-name] .

- Now, creatint a django apps
first time just create apps dir in your base dir
([your-env-name]).../DL91_event_management >>> mkdir apps

    - now make app dir which you want to create inside apps dir
    apps/[your-app-name]
([your-env-name]).../DL91_event_management >>> python manage.py startapp [your-app-name] apps\[your-app-name]

apps/[your-app-name]/apps.py

from django.apps import AppConfig
class MasterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '[apps].[your-app-name]'

- Now, go to the project/setting.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.master', # added new
    'apps.artist' # added new
]

- template integration:
apps/[your-app-name]/

first create dir - "templates" -> inside "templates" create another dir "[your-app-name]"

- static files configuration
apps/[your-app-name]/

first create dir - "static" -> inside "static" create another dir "[your-app-name]"

 - CSS
 - JS
 - Images...

Now, come to the project/settingd.py

Add this in settings.py
import os

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR / 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR / 'media')

Serving static files during development

Now, go to the projects/urls

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


- apply makemigrations and migrate
([your-env-name]).../DL91_event_management >>> python manage.py makemigrations
([your-env-name]).../DL91_event_management >>> python manage.py migrate

- Createsuperuser
([your-env-name]).../DL91_event_management >>> python manage.py  createsuperuser
Username (leave blank to use 'brijesh'): admin
Email address: admin
Error: Enter a valid email address.
Email address: admin@gmail.com
Password: ***
Password (again): ****
Error: Your passwords didn't match.
Password: ********
Password (again): ********
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.


Now, run your server

([your-env-name]).../DL91_event_management >>> python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 11, 2025 - 11:37:03
Django version 5.1.4, using settings 'project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.


- create model:

basic syntax:

class ModelName(models.Model):
    # Field Definitions
    field_name = models.FieldType(
        parameters
    )

    # Optional Meta Class
    class Meta:
        # Specify database table name
        db_table = 'custom_table_name'

        # Abstract model
        abstract = False  # Default is False; True prevents creating a table for the model

    # String representation
    def __str__(self):
        return self.some_field



# form setup:
s-1] <form action="{% url 'url_name' %}" method="post" enctype="multipart/form-data">
s-2] {% csrf_token %}
s-3] name attribute required in input fields
s-4] button type must be submit

# session and cookies:
https://witzcode.pythonanywhere.com/blog-details/cd68a82d-37e4-4ce6-a0c0-40c5cb0644b7_blog


API SETUP:
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

LIST_API
    - get all data - GET
    - insert new data - POST

DETAIL_API(ID: required)
    - get specific data - GET
    - update specific data with all fields - PUT
    - update specific data with partially fields - PATCH
    - delete specific data - DELETE