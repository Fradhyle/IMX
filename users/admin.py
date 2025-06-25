from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "phone_number",
        "surname",
        "given_name",
        "birthday",
    )
    ordering = ("phone_number",)
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("phone_number",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("phone_number",)}),)
