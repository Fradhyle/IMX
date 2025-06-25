import uuid
from typing import Final

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from branches.models import Branch
from IMX.validators import phone_number_validator


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(
        self,
        phone_number,
        surname,
        given_name,
        birthday,
        gender,
        password=None,
    ):
        user = self.model(
            phone_number=phone_number,
            surname=surname,
            given_name=given_name,
            birthday=birthday,
            gender=gender,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(
        self,
        phone_number,
        surname,
        given_name,
        birthday,
        gender,
        password=None,
    ):
        user = self.create_user(
            phone_number=phone_number,
            surname=surname,
            given_name=given_name,
            birthday=birthday,
            gender=gender,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        phone_number,
        surname,
        given_name,
        birthday,
        gender,
        password=None,
    ):
        user = self.create_user(
            surname=surname,
            phone_number=phone_number,
            given_name=given_name,
            birthday=birthday,
            gender=gender,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    GENDERS: Final[dict] = {
        1: _("남성"),
        2: _("여성"),
    }
    serial = models.BigAutoField(
        verbose_name=_("연번"),
        primary_key=True,
    )
    phone_number = models.CharField(
        verbose_name=_("전화번호"),
        max_length=14,
        validators=[
            phone_number_validator,
        ],
        unique=True,
    )
    surname = models.CharField(
        verbose_name=_("성"),
        max_length=20,
    )
    given_name = models.CharField(
        verbose_name=_("이름"),
        max_length=20,
    )
    email = models.EmailField(
        verbose_name=_("이메일 주소"),
        blank=True,
        null=True,
    )
    password = models.TextField(
        verbose_name=_("암호"),
    )
    birthday = models.DateField(
        verbose_name=_("생일"),
    )
    gender = models.PositiveIntegerField(
        verbose_name=_("성별"),
        choices=GENDERS,
    )
    is_active = models.BooleanField(
        verbose_name=_("활성화 여부"),
        default=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_("직원 여부"),
        default=False,
    )
    is_superuser = models.BooleanField(
        verbose_name=_("슈퍼유저 여부"),
        default=False,
    )
    last_login = models.DateTimeField(
        verbose_name=_("최근 로그인"),
        default=timezone.now,
    )
    date_joined = models.DateTimeField(
        verbose_name=_("가입일"),
        default=timezone.now,
    )

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.surname} {self.given_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _("이용자")
        verbose_name_plural = _("이용자")

    USERNAME_FIELD = "phone_number"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "surname",
        "given_name",
        "birthday",
        "gender",
    ]


class UserBranch(models.Model):
    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    branch = models.ForeignKey(
        Branch,
        to_field="serial",
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = _("이용자 지점")


class UserLicenseType(models.Model):
    LICENSE_TYPES: Final[dict] = {
        "1L": _("1종 대형"),
        "1O": _("1종 보통"),
        "1OA": _("1종 보통 (자동)"),
        "2O": _("2종 보통"),
        "2OA": _("2종 보통 (자동)"),
        "IL": _("장롱 면허"),
    }

    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    license_type = models.CharField(
        max_length=3,
        verbose_name=_("면허 유형"),
        choices=LICENSE_TYPES,
        null=True,
        default=None,
    )

    class Meta:
        verbose_name = _("이용자 면허 유형")


class UserPlanType(models.Model):
    PLAN_TYPES: Final[dict] = {
        "T": _("시간제"),
        "GA": _("합격 보장제"),
        "GC": _("코스 보장제"),
        "GR": _("도로 보장제"),
        "LD": _("장롱 면허"),
    }

    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    plan_type = models.CharField(
        max_length=2,
        verbose_name=_("요금제 유형"),
        choices=PLAN_TYPES,
        blank=True,
        null=True,
        default=None,
    )

    class Meta:
        verbose_name = _("이용자 요금제")
