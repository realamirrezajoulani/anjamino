from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from account.models import User
from core.models import Core
from list.models import List

# Create your models here.
class Task(Core):
    class Perority(models.TextChoices):
        VERY_HIGH = "very high", _("بسیار بالا")
        HIGH = "high", _("بالا")
        MODERATE = "moderate", _("متوسط")
        LOW = "low", _("کم")
        VERY_LOW = "very low", _("بسیار کم")
    
    title = models.CharField(max_length=50, verbose_name="عنوان")

    detail = models.TextField(default=None, max_length=512, verbose_name="جزئیات")

    perority = models.CharField(choices=Perority, default=Perority.MODERATE, verbose_name="اولویت")

    completion_status = models.BooleanField(default=False, verbose_name="انجام شده؟")

    list = models.ForeignKey(List, on_delete=models.CASCADE, verbose_name="فهرست")

    def __str__(self) -> str:
        return self.title


    class Meta(Core.Meta):
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["completion_status"]),
        ]

        ordering = ["-perority"]

        verbose_name = "وظیفه"
        verbose_name_plural = "وظیفه‌ها"
    

    def get_absolute_url(self):
        # include both list_pk and the task pk
        return reverse(
            "task:task_detail",
            kwargs={
                "list_pk": self.list_id,  # FK to List
                "pk": self.pk
            }
        )
