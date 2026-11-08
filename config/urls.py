"""Enrutamiento raíz del proyecto IVA."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("apps.institutional.urls", "institutional"), namespace="institutional")),
    path("cuentas/", include(("apps.accounts.urls", "accounts"), namespace="accounts")),
    path("academia/", include(("apps.academy.urls", "academy"), namespace="academy")),
    path("tienda/", include(("apps.commerce.urls", "commerce"), namespace="commerce")),
    path("biblioteca/", include(("apps.library.urls", "library"), namespace="library")),
    path("certificados/", include(("apps.certificates.urls", "certificates"), namespace="certificates")),
    path("herramientas/", include(("apps.tools.urls", "tools"), namespace="tools")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
