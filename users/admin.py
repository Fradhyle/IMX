from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db import models

from users.models import User, UserBranch, UserType


# Register your models here.
@admin.register(User)
@admin.register(UserBranch)
@admin.register(UserType)
@admin.action(description="선택한 이용자를 비활성화 합니다.")
def deactivate_user(modeladmin, request, queryset):
    queryset.update(is_active=False)


class UserModelAdmin(UserAdmin):
    date_hierarchy = "date_joined"

    list_display = [
        "username",
        "full_name",
        "gender",
        "license_type",
        "plan_type",
        "branch",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    ]

    list_display_links = [
        "username",
        "full_name",
    ]

    list_editable = [
        "gender",
        "license_type",
        "plan_type",
        "branch",
        "is_active",
        "is_staff",
        "is_superuser",
    ]

    list_filter = (
        "gender",
        "license_type",
        "plan_type",
        "branch",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    fieldsets = [
        (
            "이용자 기본 정보",
            {
                "fields": [
                    "username",
                    "password",
                    "branch",
                    "license_type",
                    "plan_type",
                ],
            },
        ),
        (
            "개인 정보",
            {
                "fields": [
                    "full_name",
                    "birthday",
                    "gender",
                    "phone",
                ],
            },
        ),
        (
            "권한",
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ],
            },
        ),
    ]

    add_fieldsets = [
        (
            "이용자 기본 정보",
            {
                "fields": (
                    "username",
                    "password",
                    "branch",
                    "license_type",
                    "plan_type",
                ),
            },
        ),
        (
            "개인 정보",
            {
                "fields": (
                    "full_name",
                    "birthday",
                    "gender",
                    "phone",
                ),
            },
        ),
        (
            "권한",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    # "groups",
                ),
            },
        ),
    ]

    search_fields = [
        "username",
        "full_name",
    ]

    ordering = [
        "branch",
        "date_joined",
    ]

    filter_horizontal = []

    actions = [
        deactivate_user,
    ]

    # formfield_overrides = {
    #     models.TextField: {
    #         "widget": forms.TextInput(
    #             attrs={
    #                 "size": "6",
    #             },
    #         )
    #     },
    # }


admin.site.unregister(Group)
