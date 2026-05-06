from django.contrib import admin
from .models import Branch


# Register your models here.
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone_number",
    )
    list_display_links = ("name",)
    list_filter = ("is_active",)
    search_fields = ("name", "phone_number")
    ordering = ("name",)

    fieldsets = (
        (
            "기본 정보",
            {"fields": ("name",)},
        ),
        ("연락처 정보", {"fields": ("phone_number",)}),
        (
            "주소 정보",
            {
                "fields": (
                    "zip_code",
                    "address1",
                    "address2",
                )
            },
        ),
    )
