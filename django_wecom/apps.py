from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "django_wecom"
    verbose_name = _("Authentication and Authorization")
