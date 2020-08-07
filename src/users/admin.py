from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from . import models

# We don't use groups.
admin.site.unregister(Group)


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """Admin class for User model."""
    list_display = (
        'username',
        'email',
        'is_active',
        'is_staff',
        'is_superuser',
    )

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'email',
                    'phone',
                    'password',
                )
            }
        ),
        (
            _('Personal info'),
            {
                'fields': (
                    'first_name',
                    'patronymic_name',
                    'last_name',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                ),
            }
        ),
    )

    ordering = (
        'id',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
