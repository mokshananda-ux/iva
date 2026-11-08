"""Evaluaciones: quizzes, preguntas, opciones e intentos."""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class Quiz(TimeStampedModel):
    lesson = models.ForeignKey(
        "academy.Lesson", on_delete=models.CASCADE, related_name="quizzes"
    )
    title = models.CharField(max_length=200)
    pass_score = models.PositiveIntegerField(
        _("calificación mínima"), default=70,
        help_text=_("Porcentaje requerido para aprobar."),
    )

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class Question(TimeStampedModel):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class AnswerOption(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)


class QuizAttempt(TimeStampedModel):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="attempts"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="quiz_attempts",
    )
    score = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)

    def evaluate(self, selected_option_ids: list[int]) -> "QuizAttempt":
        """Calcula la calificación y marca aprobado según pass_score."""
        questions = self.quiz.questions.prefetch_related("options")
        total = questions.count() or 1
        correct = 0
        for question in questions:
            right = set(question.options.filter(is_correct=True).values_list("id", flat=True))
            chosen = right & set(selected_option_ids)
            if right and chosen == right:
                correct += 1
        self.score = round(correct * 100 / total)
        self.passed = self.score >= self.quiz.pass_score
        self.save(update_fields=["score", "passed", "updated_at"])
        return self
