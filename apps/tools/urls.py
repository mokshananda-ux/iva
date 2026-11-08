from django.urls import path

from . import views

urlpatterns = [
    path("transliterar/", views.transliterate, name="transliterate"),
]
