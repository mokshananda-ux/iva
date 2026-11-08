"""Integración con Stripe Checkout y verificación de pagos.

Principios:
- La activación de matrícula NO se dispara al volver a la página de éxito.
- Se dispara al recibir y verificar el webhook correspondiente.
- Los eventos se procesan de forma idempotente (ProcessedWebhookEvent).
"""
from __future__ import annotations

from django.conf import settings
from django.db import IntegrityError, transaction

from apps.academy.models import Enrollment
from apps.academy.services import activate_enrollment

from .models import Order, Payment, ProcessedWebhookEvent

try:  # Stripe es una dependencia opcional hasta que se integre de verdad.
    import stripe
except ImportError:  # pragma: no cover
    stripe = None


def create_checkout_session(order: Order, success_url: str, cancel_url: str):
    """Crea una sesión de Stripe Checkout para una orden pendiente."""
    if stripe is None:
        raise RuntimeError("La librería 'stripe' no está instalada.")
    stripe.api_key = settings.STRIPE_SECRET_KEY
    line_items = []
    for item in order.items.all():
        name = item.course.title if item.course else item.product.title
        line_items.append({
            "price_data": {
                "currency": order.currency,
                "product_data": {"name": name},
                "unit_amount": int(item.unit_price_mxn * 100),
            },
            "quantity": item.quantity,
        })
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=line_items,
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=str(order.pk),
    )
    order.stripe_session_id = session.id
    order.save(update_fields=["stripe_session_id", "updated_at"])
    return session


@transaction.atomic
def handle_checkout_completed(event: dict) -> bool:
    """Procesa checkout.session.completed de forma idempotente.

    Devuelve True si se procesó ahora; False si ya estaba procesado.
    """
    event_id = event["id"]
    try:
        ProcessedWebhookEvent.objects.create(event_id=event_id)
    except IntegrityError:
        # Ya procesado: idempotencia garantizada.
        return False

    session = event["data"]["object"]
    order_id = session.get("client_reference_id")
    order = Order.objects.select_for_update().get(pk=order_id)

    if order.status != Order.Status.PAID:
        order.status = Order.Status.PAID
        order.save(update_fields=["status", "updated_at"])

    Payment.objects.get_or_create(
        order=order,
        stripe_payment_intent=session.get("payment_intent", ""),
        defaults={"amount_mxn": order.total_mxn, "succeeded": True},
    )

    # Activar matrículas de los cursos de la orden.
    for item in order.items.filter(item_type="course"):
        enrollment, _ = Enrollment.objects.get_or_create(
            user=order.user, course=item.course,
            defaults={"order": order},
        )
        enrollment.order = order
        activate_enrollment(enrollment)
    return True
