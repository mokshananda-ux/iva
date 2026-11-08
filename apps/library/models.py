"""Biblioteca: colecciones, documentos y registro de descargas.

Niveles de acceso:
- REGISTERED (Nivel 1): documentos seleccionados para usuarios registrados.
- ENROLLED  (Nivel 2): colecciones completas para inscritos.
La lectura in situ (Nivel 3) se sirve por endpoints protegidos con PDF.js.
"""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import SluggedModel, TimeStampedModel


class Collection(SluggedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class Document(TimeStampedModel):
    class AccessLevel(models.TextChoices):
        REGISTERED = "registered", _("Registrado (Nivel 1)")
        ENROLLED = "enrolled", _("Inscrito (Nivel 2)")

    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, related_name="documents"
    )
    title = models.CharField(max_length=200)
    # Ruta a archivo protegido, servido por endpoint con control de permisos.
    protected_path = models.CharField(max_length=300)
    access_level = models.CharField(
        max_length=12, choices=AccessLevel.choices, default=AccessLevel.ENROLLED
    )
    download_limit = models.PositiveIntegerField(null=True, blank=True)
    watermark_enabled = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class DownloadLog(TimeStampedModel):
    """Registro de descargas para auditoría y cuotas."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="downloads"
    )
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="downloads")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
