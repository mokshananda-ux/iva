"""Contenido institucional: historia, misión, visión, páginas legales."""
from django.db import models

from apps.core.models import SluggedModel


class Page(SluggedModel):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.title
