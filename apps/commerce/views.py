import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from . import services

try:
    import stripe
except ImportError:  # pragma: no cover
    stripe = None


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Endpoint de webhook. Verifica la firma y delega en el servicio.

    Nunca activa matrículas por el retorno del navegador: solo por aquí.
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    if stripe is None:
        return HttpResponseBadRequest("stripe no disponible")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponseBadRequest("firma inválida")

    if event["type"] == "checkout.session.completed":
        services.handle_checkout_completed(event)

    return HttpResponse(status=200)
