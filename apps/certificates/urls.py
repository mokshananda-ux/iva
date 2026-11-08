from django.urls import path

from . import views

urlpatterns = [
    path("verificar/<uuid:public_id>/", views.CertificateVerifyView.as_view(), name="verify"),
]
