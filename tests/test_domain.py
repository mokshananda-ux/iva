"""Pruebas de reglas de negocio clave (didácticas)."""
import pytest

from apps.academy.models import (
    Course, CourseModule, Enrollment, Lesson, LessonResource,
)
from apps.academy.services import mandatory_lessons_completed, mark_lesson_progress
from apps.commerce.models import Order, ProcessedWebhookEvent

pytestmark = pytest.mark.django_db


def _build_course_with_mandatory_video():
    course = Course.objects.create(title="Sánscrito I", slug="sanscrito-1", is_published=True)
    module = CourseModule.objects.create(course=course, title="M1", order=1)
    lesson = Lesson.objects.create(module=module, title="L1", order=1)
    LessonResource.objects.create(lesson=lesson, kind="video", is_mandatory=True)
    return course, lesson


def test_lesson_requires_mandatory_video(django_user_model):
    user = django_user_model.objects.create_user(email="a@b.com", password="x")
    course, lesson = _build_course_with_mandatory_video()
    enrollment = Enrollment.objects.create(
        user=user, course=course, status=Enrollment.Status.ACTIVE
    )
    assert mandatory_lessons_completed(enrollment) is False
    mark_lesson_progress(enrollment, lesson, video_watched=True)
    assert mandatory_lessons_completed(enrollment) is True


def test_is_enrolled_is_computed(django_user_model):
    user = django_user_model.objects.create_user(email="c@d.com", password="x")
    course, _ = _build_course_with_mandatory_video()
    assert user.is_enrolled is False
    Enrollment.objects.create(user=user, course=course, status=Enrollment.Status.ACTIVE)
    assert user.is_enrolled is True


def test_webhook_event_is_idempotent():
    ProcessedWebhookEvent.objects.create(event_id="evt_1")
    with pytest.raises(Exception):
        ProcessedWebhookEvent.objects.create(event_id="evt_1")
