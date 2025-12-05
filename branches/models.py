from tabnanny import verbose
from typing import Final

from django.db import models

from IMX.validators import phone_number_validator


# Create your models here.
class Branch(models.Model):
    name: models.CharField = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="지점명",
    )
    address: models.CharField = models.CharField(
        max_length=255,
        verbose_name="주소",
    )
    phone_number: models.CharField = models.CharField(
        max_length=15,
        validators=[phone_number_validator],
        verbose_name="전화번호",
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="생성일",
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True,
        verbose_name="수정일",
    )
    is_active: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="운영 여부",
    )

    class Meta:
        verbose_name: str = "지점"
        verbose_name_plural: str = "지점"

    def __str__(self) -> str:
        if self.name.endswith("점"):
            return self.name
        else:
            return f"{self.name}점"


# Following model is created by Google Gemini and it's not verified by human yet.
class BranchDetail(models.Model):
    branch: models.OneToOneField = models.OneToOneField(
        Branch,
        on_delete=models.CASCADE,
        related_name="detail",
        verbose_name="지점",
    )

    # 운영 시간
    weekday_open_time = models.TimeField(verbose_name="평일 시작 시간")
    weekday_close_time = models.TimeField(verbose_name="평일 종료 시간")
    weekend_open_time = models.TimeField(
        verbose_name="주말 시작 시간", null=True, blank=True
    )
    weekend_close_time = models.TimeField(
        verbose_name="주말 종료 시간", null=True, blank=True
    )

    # 수업 시간 구조 (Timetable Structure)
    lesson_duration_min = models.PositiveSmallIntegerField(
        default=50,
        verbose_name="수업 시간(분)",
    )
    break_duration_min = models.PositiveSmallIntegerField(
        default=10,
        verbose_name="쉬는 시간(분)",
    )

    # 📌 장비 대수 (최대 동시 이용 가능 인원)
    max_capacity = models.PositiveSmallIntegerField(
        verbose_name="최대 동시 이용 가능 인원",
        help_text="해당 지점에서 한 시간에 예약 가능한 총 슬롯 수입니다.",
    )

    class Meta:
        verbose_name = "지점 운영 정보"
        verbose_name_plural = "지점 운영 정보"

    def __str__(self):
        return f"{self.branch.name} 운영 정보"
