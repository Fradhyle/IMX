from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(
    regex=r"^\d{2,4}-?\d{3,4}-?\d{4}$",
    message="올바른 전화번호 형식이 아닙니다.",
)
