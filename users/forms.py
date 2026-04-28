from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CreateUserForm(UserCreationForm):
    """
    이용자를 생성할 때 이용하는 폼입니다.
    """

    class Meta:
        model = User
        fields = (
            "phone_number",
            "surname",
            "given_name",
            "birth_date",
            "gender",
        )
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ChangeUserForm(UserChangeForm):
    """
    이용자를 수정할 때 이용하는 폼입니다.
    """

    class Meta:
        model = User
        fields = (
            "phone_number",
            "surname",
            "given_name",
            "birth_date",
            "gender",
            "is_active",
            "is_staff",
        )
