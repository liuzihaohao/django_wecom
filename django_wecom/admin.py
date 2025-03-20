from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.translation import gettext_lazy as _

# 将默认 Group 注册取消
from django.contrib.auth.models import Group
admin.site.unregister(Group)

from .forms import UserChangeForm
from .models import *

class UserAdmin(UserAdmin):
    """
    管理用户
    """
    fieldsets = (
        (None, {"fields": ("username", "password",)}),
        (_("Personal info"), {"fields": ("real_name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("id", "username", "password1", "password2"),
            },
        ),
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    list_display = ("id", "username", "real_name", "is_staff", "is_active")
    ordering = ("id",)

    form = UserChangeForm

admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)