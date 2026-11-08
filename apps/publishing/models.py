"""Catálogo editorial. Administra los LIBROS (no las transacciones)."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import SluggedModel, TimeStampedModel


class Product(SluggedModel):
    """Producto base del catálogo (clase tabla concreta, herencia multi-tabla)."""

    class Format(models.TextChoices):
        DIGITAL = "digital", _("Digital")
        PHYSICAL = "physical", _("Físico")
        BOTH = "both", _("Ambos formatos")

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price_mxn = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available_format = models.CharField(
        max_length=10, choices=Format.choices, default=Format.DIGITAL
    )
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class DigitalBook(TimeStampedModel):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="digital"
    )
    # Archivo protegido; nunca se sirve directo desde MEDIA público.
    protected_path = models.CharField(max_length=300)
    download_limit = models.PositiveIntegerField(
        null=True, blank=True,
        help_text=_("Nulo = sin límite. Permite limitar descargas por política."),
    )


class PhysicalBook(TimeStampedModel):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="physical"
    )
    stock = models.PositiveIntegerField(default=0)
    weight_grams = models.PositiveIntegerField(default=0)
