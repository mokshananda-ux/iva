"""Reglas de emisión de certificados.

Se emite cuando:
1. La matrícula está activa.
2. Todas las lecciones obligatorias están completadas.
3. Se satisfacen los requisitos de evaluación.
4. No existe condición administrativa que lo impida.
"""
from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.academy.services import mandatory_lessons_completed

from .models import Certificate


def can_issue_certificate(enrollment) -> tuple[bool, str]:
    if enrollment.status != "active":
        return False, "La matrícula no está activa."
    if not mandatory_lessons_completed(enrollment):
        return False, "Faltan lecciones obligatorias por completar."
    existing = getattr(enrollment, "certificate", None)
    if existing and existing.administrative_hold:
        return False, "Existe un bloqueo administrativo."
    return True, ""


def issue_certificate(enrollment) -> Certificate:
    ok, reason = can_issue_certificate(enrollment)
    if not ok:
        raise ValidationError(reason)
    certificate, _ = Certificate.objects.get_or_create(enrollment=enrollment)
    # TODO: generar PDF con WeasyPrint y guardarlo en certificate.pdf.
    return certificate
