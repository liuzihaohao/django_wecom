# Django Wecom

[![](https://img.shields.io/github/actions/workflow/status/liuzihaohao/django_wecom/release.yml?style=flat-square&label=Build%20and%20Publish%20Python%20Package)](https://github.com/liuzihaohao/django_wecom/actions/workflows/release.yml)

[![](https://img.shields.io/pypi/v/django_wecom?style=flat-square)](https://pypi.org/project/django-wecom/)

## Install

`pip install django_wecom`

## Usage

1. Register App in `setting.py`
2. Write a url in `urls.py`, `path('auth/', include('django_wecom.urls'))`
3. Set the user data table in `setting.py`, `AUTH_USER_MODEL = "django_wecom.User"`
4. Migrate the database, `python manage.py migrate django_wecom`
5. If your template need `is_in_wecom` tag, you can write this in `settings.py`
    ```python
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django_wecom.context_processors.get_var',
                    ...
                ],
            },
        },
    ]
    ```
6. If you want add some new fields in User or Group table, you can inherit the `django_wecom.models.User` or `django_wecom.models.Group`, but remember change `AUTH_USER_MODEL = "your_app.User"` in `settings.py`

