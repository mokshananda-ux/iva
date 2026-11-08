"""Foros de discusión por lección."""
from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class Thread(TimeStampedModel):
    lesson = models.ForeignKey(
        "academy.Lesson", on_delete=models.CASCADE, related_name="threads"
    )
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="threads"
    )

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class Post(TimeStampedModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    body = models.TextField()
