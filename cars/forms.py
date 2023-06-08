from typing import Any

from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from captcha.fields import CaptchaField
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from cars import models


class CallBackForm(ModelForm[models.CallBack]):
    captcha = CaptchaField()

    class Meta:
        model = models.CallBack
        fields = ["full_name", "phone", "comment", "captcha"]
        widgets = {"comment": forms.Textarea({"rows": 3})}


class ReviewForm(ModelForm[models.Review]):
    captcha = CaptchaField()

    class Meta:
        model = models.Review
        fields = ["rating", "text"]
        widgets = {"text": forms.Textarea({"rows": 5})}


class PostSearchForm(forms.Form):
    q = forms.Field(
        widget=forms.TextInput(
            {
                "class": "form-control",
                "placeholder": _("Search"),
            }
        ),
        label=_("Search"),
    )


class TestDriveForm(ModelForm[models.TestDrive]):
    class Meta:
        model = models.TestDrive
        fields = ["phone", "text", "date"]
        widgets = {
            "text": forms.Textarea({"rows": 3}),
            "date": DateTimePickerInput(options={"format": "DD.MM.YYYY HH:mm"}),
        }
