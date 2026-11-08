"""Reglas de negocio del dominio académico."""
from __future__ import annotations

from django.utils import timezone

from .models import Enrollment, Lesson, LessonProgress


def activate_enrollment(enrollment: Enrollment) -> Enrollment:
    """Activa una matrícula tras verificar el pago (llamada desde el webhook)."""
    if enrollment.status != Enrollment.Status.ACTIVE:
        enrollment.status = Enrollment.Status.ACTIVE
        enrollment.activated_at = timezone.now()
        enrollment.save(update_fields=["status", "activated_at", "updated_at"])
    return enrollment


def mark_lesson_progress(enrollment: Enrollment, lesson: Lesson, **flags) -> LessonProgress:
    progress, _ = LessonProgress.objects.get_or_create(
        enrollment=enrollment, lesson=lesson
    )
    for field, value in flags.items():
        setattr(progress, field, value)
    if progress.is_complete and progress.completed_at is None:
        progress.completed_at = timezone.now()
    progress.save()
    return progress


def mandatory_lessons_completed(enrollment: Enrollment) -> bool:
    """¿Todas las lecciones obligatorias del curso están completadas?"""
    lessons = Lesson.objects.filter(module__course=enrollment.course)
    for lesson in lessons:
        progress = enrollment.progress.filter(lesson=lesson).first()
        if progress is None or not progress.is_complete:
            return False
    return True
