from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ChangeUserForm, CreateUserForm
from .models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CreateUserForm
    form = ChangeUserForm

    # 목록 페이지에 표시할 필드
    list_display = (
        "phone_number",
        "full_name",
        "birth_date",
        "gender",
        "is_staff",
        "is_active",
    )
    # 상세 페이지에서 클릭 가능한 필드
    list_display_links = (
        "phone_number",
        "full_name",
    )
    # 검색 기능 (전화번호와 이름으로 검색 가능)
    search_fields = (
        "phone_number",
        "surname",
        "given_name",
    )
    # 정렬 순서
    ordering = ("-date_joined",)

    # 상세 페이지의 섹션 구성
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("개인정보", {"fields": ("surname", "given_name", "birth_date", "gender")}),
        (
            "권한 및 상태",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("중요 일자", {"fields": ("last_login", "date_joined")}),
    )

    # 사용자 추가 페이지의 섹션 구성
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "surname",
                    "given_name",
                    "birth_date",
                    "gender",
                    "password",
                ),
            },
        ),
    )

    # 데코레이터를 사용하여 컬럼 헤더 이름 지정
    @admin.display(description="성명")
    def full_name(self, obj):
        return obj.full_name
