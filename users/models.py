from branches.models import Branch
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
phone_validator = RegexValidator(
    regex=r"\d{2,4}-?\d{3,4}-?\d{4}",
    message="올바른 전화번호 형식이 아닙니다.",
)


class UserManager(BaseUserManager):
    def create_user(
        self,
        username,
        given_name,
        surname,
        birthday,
        gender,
        phone_number,
        branch,
        password=None,
        **kwargs,
    ):
        user = self.model(
            username=username,
            given_name=given_name,
            surname=surname,
            birthday=birthday,
            gender=gender,
            phone_number=phone_number,
            branch=Branch.objects.get(srl=branch),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(
        self,
        username,
        given_name,
        surname,
        birthday,
        gender,
        phone_number,
        branch,
        password=None,
        **kwargs,
    ):
        user = self.create_user(
            username=username,
            given_name=given_name,
            surname=surname,
            birthday=birthday,
            gender=gender,
            phone_number=phone_number,
            branch=branch,
            password=password,
            **kwargs,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username,
        given_name,
        surname,
        birthday,
        gender,
        phone_number,
        branch,
        password,
        **kwargs,
    ):
        user = self.create_user(
            username=username,
            given_name=given_name,
            surname=surname,
            birthday=birthday,
            gender=gender,
            phone_number=phone_number,
            branch=branch,
            password=password,
            **kwargs,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    GENDERS = {
        1: _("Male"),
        2: _("Female"),
    }

    username = models.CharField(verbose_name=_("username"), max_length=20, unique=True)
    given_name = models.CharField(verbose_name=_("given_name"), max_length=20)
    surname = models.CharField(verbose_name=_("surname"), max_length=20)
    email = models.EmailField(verbose_name=_("email address"), blank=True, null=True)
    password = models.TextField(verbose_name=_("password"))
    birthday = models.DateField(verbose_name=_("birthday"))
    gender = models.PositiveIntegerField(verbose_name=_("gender"), choices=GENDERS)
    phone_number = models.CharField(
        verbose_name=_("phone_number"), max_length=14, validators=[phone_validator]
    )
    branch = models.ForeignKey(
        to="branches.Branch",
        verbose_name=_("branch"),
        on_delete=models.SET_DEFAULT,
        default=1,
    )
    is_active = models.BooleanField(verbose_name="계정 상태", default=True)
    is_staff = models.BooleanField(verbose_name="직원 여부", default=False)
    is_superuser = models.BooleanField(verbose_name="최고관리자 여부", default=False)
    last_login = models.DateTimeField(
        verbose_name="최종 접속 일시", default=timezone.now
    )
    date_joined = models.DateTimeField(verbose_name="가입 일시", default=timezone.now)

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.surname} {self.given_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "이용자"
        verbose_name_plural = "이용자"

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "branch",
        "given_name",
        "surname",
        "birthday",
        "gender",
        "phone_number",
    ]


class UserBranch(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, to_field="srl", on_delete=models.DO_NOTHING)


class UserType(models.Model):
    LICENSE_TYPES = {
        "1L": "1종 대형",
        "1O": "1종 보통",
        "1OA": "1종 보통 (자동)",
        "2O": "2종 보통",
        "2OA": "2종 보통 (자동)",
        "P": "장롱 면허",
    }
    PLAN_TYPES = {
        "T": "시간제",
        "GA": "합격 보장제",
        "GC": "기능 보장제",
        "GR": "도로주행 보장제",
        "P": "장롱 면허",
    }

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    license_type = models.CharField(
        max_length=3,
        verbose_name="면허 종류",
        choices=LICENSE_TYPES,
        blank=True,
        null=True,
        default=None,
    )
    plan_type = models.CharField(
        max_length=2,
        verbose_name="요금제 유형",
        choices=PLAN_TYPES,
        blank=True,
        null=True,
        default=None,
    )
