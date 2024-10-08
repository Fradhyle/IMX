import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

# Create your models here.
phone_validator = RegexValidator(
    regex=r"\d{2,4}-?\d{3,4}(-?\d{4})?",
    message="올바른 전화번호 형식이 아닙니다.",
)


class Branch(models.Model):
    srl = models.BigAutoField(
        verbose_name="연번",
        primary_key=True,
    )
    name = models.CharField(
        verbose_name="지점명",
        unique=True,
        max_length=255,
    )
    equipment_count = models.PositiveIntegerField(
        verbose_name="장비 대수",
        default=5,
    )
    postcode = models.CharField(
        verbose_name="우편번호",
        max_length=5,
    )
    address1 = models.CharField(
        verbose_name="도로명 주소",
        max_length=255,
    )
    address2 = models.CharField(
        verbose_name="상세 주소",
        blank=True,
        max_length=255,
    )
    phone1 = models.CharField(
        verbose_name="전화번호 1",
        max_length=14,
        validators=[
            phone_validator,
        ],
    )
    phone2 = models.CharField(
        verbose_name="전화번호 2",
        max_length=14,
        validators=[
            phone_validator,
        ],
        blank=True,
    )
    is_open = models.BooleanField(
        verbose_name="폐업 여부",
        default=True,
        choices=(
            (True, "개업"),
            (False, "폐업"),
        ),
    )
    lesson_time = models.DurationField(
        verbose_name="수업 시간",
        default=datetime.timedelta(minutes=110),
    )
    break_time = models.DurationField(
        verbose_name="쉬는 시간",
        default=datetime.timedelta(minutes=10),
    )

    class Meta:
        verbose_name = "지점"
        verbose_name_plural = "지점"
        ordering = [
            "srl",
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("branches:detail", kwargs={"srl": self.srl})


class BusinessHour(models.Model):
    srl = models.BigAutoField(
        verbose_name="연번",
        primary_key=True,
    )
    branch = models.ForeignKey(
        "branches.Branch",
        on_delete=models.CASCADE,
        verbose_name="지점",
    )
    is_weekday = models.BooleanField(
        verbose_name="평일 여부",
        default=True,
        choices=(
            (True, "평일"),
            (False, "휴일"),
        ),
    )
    open_time = models.TimeField(
        verbose_name="개점 시간",
        default=datetime.time(9, 0),
    )
    close_time = models.TimeField(
        verbose_name="폐점 시간",
        default=datetime.time(23, 0),
    )

    class Meta:
        verbose_name = "영업 시간"
        verbose_name_plural = "영업 시간"
        ordering = [
            "branch",
            "is_weekday",
            "open_time",
        ]
        unique_together = [
            "branch",
            "is_weekday",
        ]

    # def get_absolute_url(self):
    #     return reverse("branches:hours", kwargs={"branch": self.branch.srl})


class Timetable(models.Model):
    srl = models.BigAutoField(
        primary_key=True,
        verbose_name="연번",
    )
    branch = models.ForeignKey(
        "branches.Branch",
        on_delete=models.CASCADE,
        verbose_name="지점",
    )
    is_weekday = models.BooleanField(
        verbose_name="평일 여부",
        default=True,
        choices=(
            (True, "평일"),
            (False, "휴일"),
        ),
    )
    period = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        verbose_name="교시",
    )
    start_time = models.TimeField(
        verbose_name="시작 시간",
    )
    end_time = models.TimeField(
        verbose_name="종료 시간",
    )

    class Meta:
        verbose_name = "시간표"
        verbose_name_plural = "시간표"
        ordering = [
            "branch",
            "is_weekday",
            "period",
        ]
        unique_together = [
            "branch",
            "is_weekday",
            "period",
        ]

    # def get_absolute_url(self):
    #     return reverse("timetables:detail", kwargs={"branch": self.branch.srl})
