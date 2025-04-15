from typing import Final
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

    username = models.CharField(verbose_name=_("Username"), max_length=20, unique=True,)
    given_name = models.CharField(verbose_name=_("Given Name"), max_length=20,)
    surname = models.CharField(verbose_name=_("Surname"), max_length=20,)
    email = models.EmailField(verbose_name=_("Email Address"), blank=True, null=True,)
    password = models.TextField(verbose_name=_("Password"),)
    birthday = models.DateField(verbose_name=_("Birthday"),)
    gender = models.PositiveIntegerField(verbose_name=_("Gender"), choices=GENDERS,)
    phone_number = models.CharField(verbose_name=_("Phone Number"), max_length=14, validators=[phone_validator],)
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True,)
    is_staff = models.BooleanField(verbose_name=_("Is Staff"), default=False,)
    is_superuser = models.BooleanField(verbose_name=_("Is Superuser"), default=False,)
    last_login = models.DateTimeField(verbose_name=_("Last Login"), default=timezone.now,)
    date_joined = models.DateTimeField(verbose_name=_("Date Joined"), default=timezone.now,)

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.surname} {self.given_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "given_name",
        "surname",
        "birthday",
        "gender",
        "phone_number",
    ]


class UserBranch(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, to_field="srl", on_delete=models.DO_NOTHING)


class UserLicenseType(models.Model):
    LICENSE_TYPES: Final[dict] = {
        "1L": _("License 1L"),
        "1O": _("License 1O"),
        "1OA": _("License 1OA"),
        "2O": _("License 2O"),
        "2OA": _("License 2OA"),
        "LD": _("License LD"),
    }

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    license_type = models.CharField(
        max_length=3,
        verbose_name=_("License Type"),
        choices=LICENSE_TYPES,
        blank=True,
        null=True,
        default=None,
    )

class UserPlanType(models.Model):
    PLAN_TYPES: Final[dict] = {
        "T": _("Plan T"),
        "GA": _("Plan GA"),
        "GC": _("Plan GC"),
        "GR": _("Plan GR"),
        "LD": _("Plan LD"),
    }

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_type = models.CharField(
        max_length=2,
        verbose_name=_("Plan Type"),
        choices=PLAN_TYPES,
        blank=True,
        null=True,
        default=None,
    )
