"""Modelos y mixins comunes reutilizables."""
from django.db import models


class TimeStampedModel(models.Model):
    """Añade marcas de creación y actualización a cualquier modelo."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SluggedModel(TimeStampedModel):
    """Modelo base con slug único para URLs legibles."""

    slug = models.SlugField(max_length=160, unique=True)

    class Meta:
        abstract = True
