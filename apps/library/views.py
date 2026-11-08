import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from apps.core.permissions import can_download_library_item

from .models import Document, DownloadLog


@login_required
def protected_download(request, pk: int):
    """Sirve un documento tras comprobar permisos en el servidor.

    Toda descarga pasa por esta comprobación y queda registrada.
    """
    document = get_object_or_404(Document, pk=pk)
    if not can_download_library_item(request.user, document):
        raise PermissionDenied("No tienes permiso para descargar este documento.")

    # Cuota opcional por política editorial.
    if document.download_limit is not None:
        count = DownloadLog.objects.filter(user=request.user, document=document).count()
        if count >= document.download_limit:
            raise PermissionDenied("Has alcanzado el límite de descargas.")

    path = os.path.join(settings.PROTECTED_MEDIA_ROOT, document.protected_path)
    if not os.path.exists(path):
        raise Http404("Archivo no encontrado.")

    DownloadLog.objects.create(
        user=request.user, document=document,
        ip_address=request.META.get("REMOTE_ADDR"),
    )
    return FileResponse(open(path, "rb"), as_attachment=True)
