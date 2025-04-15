import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
phone_validator = RegexValidator(
    regex=r"\d{2,4}-?\d{3,4}(-?\d{4})?",
    message="올바른 전화번호 형식이 아닙니다.",
)


class Branch(models.Model):
    srl = models.BigAutoField(
        verbose_name=_("Serial"),
        primary_key=True,
    )
    name = models.CharField(
        verbose_name=_("Branch Name"),
        unique=True,
        max_length=255,
    )
    equipment_count = models.PositiveIntegerField(
        verbose_name=_("Equipment Count"),
        default=5,
    )
    postcode = models.CharField(
        verbose_name=_("Postcode"),
        max_length=5,
    )
    address1 = models.CharField(
        verbose_name=_("Street Address"),
        max_length=255,
    )
    address2 = models.CharField(
        verbose_name=_("Detailed Address"),
        blank=True,
        max_length=255,
    )
    phone1 = models.CharField(
        verbose_name=_("Phone Number 1"),
        max_length=14,
        validators=[
            phone_validator,
        ],
    )
    phone2 = models.CharField(
        verbose_name=_("Phone Number 2"),
        max_length=14,
        validators=[
            phone_validator,
        ],
        blank=True,
    )
    is_open = models.BooleanField(
        verbose_name=_("Is Open"),
        default=True,
        choices=(
            (True, _("Open")),
            (False, _("Shut Down")),
        ),
    )

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")
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
        verbose_name = _("Branch"),
    )
    lesson_duration = models.DurationField(
        verbose_name=_("Lesson Duration"),
        default=datetime.timedelta(minutes=110),
    )
    break_duration = models.DurationField(
        verbose_name=_("Break Duration"),
        default=datetime.timedelta(minutes=10),
    )

    class Meta:
        verbose_name = _("Duration")
        verbose_name_plural = _("Durations")
        ordering = [
            "branch",
        ]


class BusinessHour(models.Model):
    branch = models.ForeignKey(
        "branches.Branch",
        on_delete=models.CASCADE,
        verbose_name = _("Branch"),
    )
    is_weekday = models.BooleanField(
        verbose_name=_("Is Weekday"),
        default=True,
        choices=(
            (True, _("Weekday")),
            (False, _("Holiday")),
        ),
    )
    open_time = models.TimeField(
        verbose_name=_("Open Time"),
        default=datetime.time(9, 0),
    )
    close_time = models.TimeField(
        verbose_name=_("Close Time"),
        default=datetime.time(23, 0),
    )

    class Meta:
        verbose_name = _("Business Hour")
        verbose_name_plural = _("Business Hours")
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
        verbose_name=_("Is Weekday"),
        default=True,
        choices=(
            (True, _("Weekday")),
            (False, _("Holiday")),
        ),
    )
    period = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        verbose_name=_("Period"),
    )
    start_time = models.TimeField(
        verbose_name=_("Start Time"),
    )
    end_time = models.TimeField(
        verbose_name=_("End Time"),
    )

    class Meta:
        verbose_name = _("Timetable")
        verbose_name_plural = _("Timetables")
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
