from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .transliteration import to_iast


@require_GET
def transliterate(request):
    """Endpoint HTMX/JSON para el transliterador devanāgarī -> IAST."""
    text = request.GET.get("text", "")
    return JsonResponse({"input": text, "iast": to_iast(text)})
