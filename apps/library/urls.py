from django.urls import path

from . import views

urlpatterns = [
    path("descargar/<int:pk>/", views.protected_download, name="download"),
]
