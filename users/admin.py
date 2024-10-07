from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.db import models

from users.models import User


# Register your models here.
@admin.action(description="선택한 이용자를 비활성화 합니다.")
def deactivate_user(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(User)
class UserModelAdmin(UserAdmin):
    pass
