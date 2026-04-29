from pyexpat import model

from django.db import models
from IMX.validators import phone_number_validator


# Create your models here.
class Branch(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="지점명",
    )
    zip_code = models.CharField(
        max_length=5,
        verbose_name="우편번호",
    )
    address1 = models.CharField(
        max_length=255,
        verbose_name="도로명주소",
    )
    address2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="상세주소",
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[phone_number_validator],
        verbose_name="전화번호",
    )

    class Meta:
        verbose_name = "지점"
        verbose_name_plural = "지점들"

    def __str__(self):
        if self.name.endswith("점"):
            return self.name
        else:
            return f"{self.name}점"
