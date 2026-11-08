"""Emisión y validación de certificados."""
from __future__ import annotations

import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class Certificate(TimeStampedModel):
    """Certificado ligado a una matrícula concreta.

    Tiene identificador único y una página pública de verificación.
    """

    enrollment = models.OneToOneField(
        "academy.Enrollment", on_delete=models.PROTECT,
        related_name="certificate",
    )
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to="certificates/", blank=True, null=True)
    # Bloqueo administrativo que impide la emisión/validez.
    administrative_hold = models.BooleanField(_("bloqueo administrativo"), default=False)

    def __str__(self) -> str:  # pragma: no cover
        return f"Certificado {self.public_id}"

    def get_verify_url(self) -> str:
        return reverse("certificates:verify", args=[self.public_id])

    @property
    def is_valid(self) -> bool:
        return not self.administrative_hold
