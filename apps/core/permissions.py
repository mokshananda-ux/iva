"""Comprobaciones de autorización centralizadas.

Regla de oro del proyecto: la autorización se verifica SIEMPRE en el
servidor. La interfaz solo oculta/ muestra; nunca es la fuente de verdad.
"""
from __future__ import annotations

from django.core.exceptions import PermissionDenied


def require_authenticated(user) -> None:
    if not user.is_authenticated:
        raise PermissionDenied("Se requiere iniciar sesión.")


def can_access_course(user, course) -> bool:
    """¿Puede el usuario ver el contenido completo de un curso?

    Verdadero si tiene una matrícula activa en ese curso, o si es staff /
    instructor. El cálculo se basa en datos, no en roles persistentes.
    """
    if not user.is_authenticated:
        return False
    if user.is_staff or getattr(user, "is_instructor", False):
        return True
    return user.enrollments.filter(course=course, status="active").exists()


def can_download_library_item(user, item) -> bool:
    """Comprobación de permiso para descargas de biblioteca.

    Nivel 1 (registrado): solo documentos marcados como públicos-registrados.
    Nivel 2 (inscrito): colecciones completas.
    """
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    if item.access_level == item.AccessLevel.REGISTERED:
        return True
    if item.access_level == item.AccessLevel.ENROLLED:
        return user.is_enrolled
    return False
