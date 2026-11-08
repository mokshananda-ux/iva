"""Materiales educativos y recursos descargables (no ligados a una lección)."""
from django.db import models

from apps.core.models import TimeStampedModel


class EducationalResource(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    protected_path = models.CharField(max_length=300, blank=True)
    external_url = models.URLField(blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover
        return self.title
