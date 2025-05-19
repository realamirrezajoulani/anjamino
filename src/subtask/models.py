from django.db import models
from django.urls import reverse

from core.models import Core
from task.models import Task

# Create your models here.
class Subtask(Core):
    title = models.CharField(max_length=50, verbose_name="عنوان")

    completion_status = models.BooleanField(default=False, verbose_name="انجام شده؟")

    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="وظیفه")

    def __str__(self) -> str:
        return self.title

    class Meta(Core.Meta):
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["completion_status"]),
        ]

        verbose_name = "خرده‌وظیفه"
        verbose_name_plural = "خرده‌وظیفه‌ها"
    
    def get_absolute_url(self):
        return reverse(
            "subtask:subtask_detail",
            kwargs={
                "task_pk": self.task_id,
                "pk": self.pk
            }
        )