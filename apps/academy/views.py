from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from apps.core.permissions import can_access_course

from .models import Course, Lesson


class CourseListView(ListView):
    model = Course
    template_name = "academy/course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.filter(is_published=True)


class CourseDetailView(DetailView):
    model = Course
    template_name = "academy/course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["has_access"] = can_access_course(self.request.user, self.object)
        return ctx


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "academy/lesson_detail.html"
    context_object_name = "lesson"

    def get_object(self, queryset=None):
        lesson = get_object_or_404(Lesson, pk=self.kwargs["pk"])
        course = lesson.module.course
        # Autorización en servidor: muestra libre, resto segun matrícula.
        if lesson.is_sample:
            return lesson
        if not can_access_course(self.request.user, course):
            raise PermissionDenied("Necesitas una matrícula activa.")
        return lesson
