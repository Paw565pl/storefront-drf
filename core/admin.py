from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    readonly_fields = ["date_joined", "last_login"]
    list_display = ["username", "email", "is_staff"]
    search_fields = ["username", "email"]
    fieldsets = [
        [None, {"fields": ["username", "email", "password"]}],
        [
            "Permissions",
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ],
            },
        ],
        ["Important dates", {"fields": ["last_login", "date_joined"]}],
    ]
    add_fieldsets = [
        [
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "username",
                    "email",
                    "password1",
                    "password2",
                ],
            },
        ],
    ]
