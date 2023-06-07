from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=_("email address"),
        help_text=_("Enter a valid email address"),
        unique=True,
    )
