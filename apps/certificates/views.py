from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from .models import Certificate


class CertificateVerifyView(DetailView):
    """Página pública para verificar autenticidad por public_id."""

    model = Certificate
    template_name = "certificates/verify.html"
    context_object_name = "certificate"

    def get_object(self, queryset=None):
        return get_object_or_404(Certificate, public_id=self.kwargs["public_id"])
