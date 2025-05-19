from uuid import uuid4
from django.db import models

# Create your models here.
class Core(models.Model):
    """Abstract base class that adds core fields to models."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

        ordering = ["-created_at"]