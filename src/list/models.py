from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from account.models import User
from core.models import Core

# Create your models here.
class List(Core):
    class Color(models.TextChoices):
        RED = "red", _("قرمز")
        GREEN = "green", _("سبز")
        YELLOW = "yellow", _("زرد")
        BLUE = "blue", _("آبی")
        MAGENTA = "magenta", _("سرخابی")

        __empty__ = "پیش‌فرض"

    title = models.CharField(max_length=50, verbose_name="عنوان")

    color = models.CharField(choices=Color, default=Color.__empty__, verbose_name="رنگ")

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")

    def __str__(self) -> str:
        return self.title

    class Meta(Core.Meta):
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["color"]),
        ]

        verbose_name = "فهرست"
        verbose_name_plural = "فهرست‌ها"
    
    def get_absolute_url(self):
        return reverse("list:list_detail", kwargs={"pk": self.pk})
    