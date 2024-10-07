from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils import timezone

from branches.models import Branch

# Create your models here.
phone_validator = RegexValidator(
    regex=r"\d{2,4}-?\d{3,4}-?\d{4}",
    message="올바른 전화번호 형식이 아닙니다.",
)


class UserManager(BaseUserManager):
    def create_user(
        self,
        username,
        full_name,
        birthday,
        gender,
        phone_number,
        branch,
        password=None,
        **kwargs
    ):
        user = self.model(
            username=username,
            full_name=full_name,
            birthday=birthday,
            gender=gender,
            phone_number=phone_number,
            license_type=kwargs["license_type"],
            plan_type=kwargs["plan_type"],
            branch=Branch.objects.get(srl=branch),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staff(
        self, username, full_name, birthday, gender, phone, branch, password, **kwargs
    ):
        user = self.create_user(
            username, full_name, birthday, gender, phone, branch, password, kwargs
        )
        user.staff = True
        user.save(using=self._db)

        return user

    def create_superuser(
        self, username, full_name, birthday, gender, phone, branch, password, **kwargs
    ):
        user = self.create_user(
            username, full_name, birthday, gender, phone, branch, password, kwargs
        )
        user.staff = True
        user.superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    objects = UserManager()

    GENDERS = {
        1: "남성",
        2: "여성",
    }

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

    srl = models.BigAutoField(
        primary_key=True,
        verbose_name="연번",
    )

    username = models.TextField(
        unique=True,
        verbose_name="아이디",
    )

    full_name = models.TextField(
        verbose_name="이름",
    )

    password = models.TextField(
        verbose_name="암호",
    )

    birthday = models.DateField(
        verbose_name="생년월일",
    )

    gender = models.PositiveIntegerField(
        verbose_name="성별",
        choices=GENDERS,
    )

    phone_number = models.CharField(
        verbose_name="전화번호",
        max_length=14,
        validators=[
            phone_validator,
        ],
    )

    branch = models.ForeignKey(
        to="branches.Branch",
        verbose_name="소속 지점",
        on_delete=models.SET_DEFAULT,
        default=1,
    )

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

    is_staff = models.BooleanField(
        verbose_name="직원 여부",
        default=False,
    )

    is_active = models.BooleanField(
        verbose_name="계정 상태",
        default=True,
    )

    is_superuser = models.BooleanField(
        verbose_name="최고관리자 여부",
        default=False,
    )

    last_login = models.DateTimeField(
        verbose_name="최종 접속 일시",
        default=timezone.now,
    )

    date_joined = models.DateTimeField(
        verbose_name="가입 일시",
        default=timezone.now,
    )

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = [
        "branch",
    ]
