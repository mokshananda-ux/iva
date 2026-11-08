"""Dominio educativo: cursos, módulos, lecciones, recursos, matrículas y
progreso.

Jerarquía: Course -> CourseModule -> Lesson -> LessonResource.
Una persona puede tener varias matrículas, cada una ligada a un curso y a la
verificación de pago de ESE curso.
"""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import SluggedModel, TimeStampedModel


class Course(SluggedModel):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    # Precio de referencia; la venta real vive en commerce.
    price_mxn = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class CourseModule(TimeStampedModel):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="modules"
    )
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = [("course", "order")]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.course.title} / {self.title}"


class Lesson(TimeStampedModel):
    module = models.ForeignKey(
        CourseModule, on_delete=models.CASCADE, related_name="lessons"
    )
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_sample = models.BooleanField(
        _("es lección de muestra"), default=False,
        help_text=_("Visible para registrados sin matrícula."),
    )

    class Meta:
        ordering = ["order"]
        unique_together = [("module", "order")]

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class LessonResource(TimeStampedModel):
    """Recurso adjunto a una lección. El tipo determina las reglas de avance."""

    class Kind(models.TextChoices):
        VIDEO = "video", _("Vídeo")
        PDF = "pdf", _("PDF")
        QUIZ = "quiz", _("Quiz")
        LAB = "lab", _("Lab")
        FORUM = "forum", _("Foro")

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="resources"
    )
    kind = models.CharField(max_length=10, choices=Kind.choices)
    title = models.CharField(max_length=200, blank=True)
    # URL externa (vídeo) o ruta a archivo protegido (PDF).
    external_url = models.URLField(blank=True)
    protected_path = models.CharField(max_length=300, blank=True)
    is_mandatory = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.get_kind_display()} ({self.lesson})"


class Enrollment(TimeStampedModel):
    """Matrícula independiente usuario-curso con verificación de pago."""

    class Status(models.TextChoices):
        PENDING = "pending", _("Pendiente de pago")
        ACTIVE = "active", _("Activa")
        SUSPENDED = "suspended", _("Suspendida")
        CANCELLED = "cancelled", _("Cancelada")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name="enrollments"
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    # Enlace a la orden que verificó el pago de ESTE curso.
    order = models.ForeignKey(
        "commerce.Order", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="enrollments",
    )
    activated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Una matrícula activa por par usuario-curso (ver constraint).
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"],
                condition=models.Q(status="active"),
                name="unique_active_enrollment_per_course",
            )
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user} -> {self.course} [{self.status}]"


class LessonProgress(TimeStampedModel):
    """Avance de una lección dentro de una matrícula concreta."""

    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name="progress"
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    video_watched = models.BooleanField(default=False)
    quiz_passed = models.BooleanField(default=False)
    lab_verified = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [("enrollment", "lesson")]

    @property
    def is_complete(self) -> bool:
        """Reglas de completitud declaradas en el documento de diseño.

        Vídeo obligatorio; quiz con calificación mínima; labs verificados.
        PDF complementario y foro opcional no bloquean.
        """
        resources = self.lesson.resources.all()
        needs_quiz = resources.filter(kind="quiz").exists()
        needs_lab = resources.filter(kind="lab").exists()
        has_mandatory_video = resources.filter(kind="video", is_mandatory=True).exists()

        if has_mandatory_video and not self.video_watched:
            return False
        if needs_quiz and not self.quiz_passed:
            return False
        if needs_lab and not self.lab_verified:
            return False
        return True
