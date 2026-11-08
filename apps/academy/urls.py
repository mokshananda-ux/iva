from django.urls import path

from . import views

urlpatterns = [
    path("cursos/", views.CourseListView.as_view(), name="course_list"),
    path("cursos/<slug:slug>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("leccion/<int:pk>/", views.LessonDetailView.as_view(), name="lesson_detail"),
]
