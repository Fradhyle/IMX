import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from IMX.validators import phone_number_validator


# Create your models here.
class Branch(models.Model):
    serial = models.BigAutoField(
        verbose_name=_("연번"),
        primary_key=True,
    )
    name = models.CharField(
        verbose_name=_("지점명"),
        unique=True,
        max_length=255,
    )
    equipment_count = models.PositiveIntegerField(
        verbose_name=_("장비대수"),
        default=5,
    )
    postcode = models.CharField(
        verbose_name=_("우편번호"),
        max_length=5,
    )
    street_address = models.CharField(
        verbose_name=_("도로명 주소"),
        max_length=255,
    )
    detailed_address = models.CharField(
        verbose_name=_("상세 주소"),
        blank=True,
        max_length=255,
    )
    phone_number_1 = models.CharField(
        verbose_name=_("전화번호 1"),
        max_length=14,
        validators=[
            phone_number_validator,
        ],
    )
    phone_number_2 = models.CharField(
        verbose_name=_("전화번호 2"),
        max_length=14,
        validators=[
            phone_number_validator,
        ],
        null=True,
    )
    status = models.BooleanField(
        verbose_name=_("영업 여부"),
        default=True,
        choices=(
            (True, _("영업 중")),
            (False, _("폐업")),
        ),
    )

    class Meta:
        verbose_name = _("지점")
        ordering = [
            "srl",
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("branches:detail", kwargs={"srl": self.srl})


class Duration(models.Model):
    branch = models.ForeignKey(
        to="branches.Branch",
        on_delete=models.CASCADE,
        verbose_name=_("지점"),
    )
    lesson_duration = models.DurationField(
        verbose_name=_("수업 시간"),
        default=datetime.timedelta(minutes=110),
    )
    break_duration = models.DurationField(
        verbose_name=_("휴식 시간"),
        default=datetime.timedelta(minutes=10),
    )

    class Meta:
        verbose_name = _("시간")
        ordering = [
            "branch",
        ]


class BusinessHour(models.Model):
    branch = models.ForeignKey(
        "branches.Branch",
        on_delete=models.CASCADE,
        verbose_name=_("지점"),
    )
    is_weekday = models.BooleanField(
        verbose_name=_("평일 여부"),
        default=True,
        choices=(
            (True, _("평일")),
            (False, _("휴일")),
        ),
    )
    open_time = models.TimeField(
        verbose_name=_("개점 시간"),
        default=datetime.time(9, 0),
    )
    close_time = models.TimeField(
        verbose_name=_("폐점 시간"),
        default=datetime.time(23, 0),
    )

    class Meta:
        verbose_name = _("영업 시간")
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
    serial = models.BigAutoField(
        primary_key=True,
        verbose_name=_("연번"),
    )
    branch = models.ForeignKey(
        "branches.Branch",
        on_delete=models.CASCADE,
        verbose_name=_("지점"),
    )
    is_weekday = models.BooleanField(
        verbose_name=_("평일 여부"),
        default=True,
        choices=(
            (True, _("평일")),
            (False, _("휴일")),
        ),
    )
    period = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        verbose_name=_("교시"),
    )
    start_time = models.TimeField(
        verbose_name=_("시작 시간"),
    )
    end_time = models.TimeField(
        verbose_name=_("종료 시간"),
    )

    class Meta:
        verbose_name = _("시간표")
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
