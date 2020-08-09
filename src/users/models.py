from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """User model."""
    REQUIRED_FIELDS = []

    patronymic_name = models.CharField(
        verbose_name=_('patronymic name'),
        max_length=150,
        blank=True,
    )

    address = models.TextField(
        verbose_name=_('address'),
        blank=True,
    )

    phone = PhoneNumberField(
        verbose_name=_('phone number'),
        blank=True,
    )

    email = models.EmailField(
        verbose_name=_('e-mail address'),
        blank=True,
    )

    def get_for_checkout(self):
        """Return the profile fields that will be used during checkout."""
        return {
            'first_name': self.first_name,
            'patronymic_name': self.patronymic_name,
            'last_name': self.last_name,
            'address': self.address,
            'email': self.email,
            'phone': self.phone,
        }
