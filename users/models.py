from typing import Final

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from IMX.validators import phone_number_validator


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(
        self,
        phone_number,
        surname,
        given_name,
        birth_date,
        gender,
        password=None,
        **kwargs,
    ):
        user = self.model(
            phone_number=phone_number,
            surname=surname,
            given_name=given_name,
            birth_date=birth_date,
            gender=gender,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        phone_number,
        surname,
        given_name,
        birth_date,
        gender,
        password=None,
        **kwargs,
    ):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        return self.create_user(
            phone_number, surname, given_name, birth_date, gender, password, **kwargs
        )


class User(AbstractBaseUser, PermissionsMixin):
    class Gender(models.IntegerChoices):
        MALE = 1, "남성"
        FEMALE = 2, "여성"

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            phone_number_validator,
        ],
        verbose_name="전화번호",
    )
    surname = models.CharField(
        max_length=30,
        verbose_name="성",
    )
    given_name = models.CharField(
        max_length=30,
        verbose_name="이름",
    )
    birth_date = models.DateField(
        verbose_name="생년월일",
    )
    gender = models.PositiveSmallIntegerField(
        choices=Gender.choices,
        verbose_name="성별",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="활성 상태",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="관리자 권한",
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="최고 관리자 권한",
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="가입일",
    )

    objects = UserManager()

    USERNAME_FIELD: Final[str] = "phone_number"
    REQUIRED_FIELDS: list[str] = [
        "surname",
        "given_name",
        "birth_date",
        "gender",
    ]

    class Meta:
        verbose_name: str = "사용자"
        verbose_name_plural: str = "사용자"

    @property
    def full_name(self) -> str:
        return f"{self.surname} {self.given_name}"

    def __str__(self) -> str:
        return self.full_name


class UserDetail(models.Model):
    class PlanType(models.TextChoices):
        TIM = "TIM", "시간제"
        # All Test Gurantee
        ATG = "ATG", "전체합격보장제"
        # Driving Course Test Gurantee
        CTG = "CTG", "기능시험 합격보장제"
        # On-Road Driving Exam
        # Driving Test Guarantee
        DTG = "DTG", "도로주행시험 합격보장제"

    class LicenseType(models.TextChoices):
        L1 = "1L", "1종 대형"
        O1 = "1O", "1종 보통"
        O1A = "1OA", "1종 보통 (자동)"
        O2 = "2O", "2종 보통"
        O2A = "2OA", "2종 보통 (자동)"
        # 영어에는 장롱면허를 나타내는 단어가 없어서 'Practice'로 쓰기로 함
        PRA = "PRA", "장롱면허"

    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name="detail",
    )
    plan_type = models.CharField(
        max_length=3,
        choices=PlanType.choices,
        verbose_name="요금제",
    )
    license_type = models.CharField(
        max_length=3,
        choices=LicenseType.choices,
        verbose_name="면허 종류",
    )

    class Meta:
        verbose_name = "이용자 상세 정보"
        verbose_name_plural = "이용자 상세 정보"
