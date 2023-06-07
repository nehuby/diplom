from typing import Any

from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from .models import User
from .token import token_generator


class Signup(UserCreationForm[User]):
    def send_activation_email(self, request, user) -> None:
        current_site = get_current_site(request)
        subject = _("Activate Your Account")
        message = render_to_string(
            "registration/activate_account.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": token_generator.make_token(user),
            },
        )
        user.email_user(subject, message, html_message=message)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]
