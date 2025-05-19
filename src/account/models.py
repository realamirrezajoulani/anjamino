from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = "super admin", _("ابرمدیر")
        ADMIN = "admin", _("مدیر")
        USER = "user", _("کاربر")
    
    role = models.CharField(choices=Role, default=Role.USER, max_length=20, verbose_name="نقش")

    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return self.username