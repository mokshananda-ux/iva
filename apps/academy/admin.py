from django.contrib import admin

from .models import (
    Course, CourseModule, Enrollment, Lesson, LessonProgress, LessonResource,
)


class ModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 0


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


class ResourceInline(admin.TabularInline):
    model = LessonResource
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "price_mxn")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order", "is_sample")
    inlines = [ResourceInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "status", "activated_at")
    list_filter = ("status",)


admin.site.register(LessonProgress)
