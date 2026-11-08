"""Operaciones comerciales: carrito, órdenes, pagos, reembolsos.

commerce administra las TRANSACCIONES; publishing administra los productos.
La activación de matrícula ocurre SOLO tras verificar el webhook de Stripe.
"""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class Cart(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="carts"
    )
    is_open = models.BooleanField(default=True)


class Order(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pendiente")
        PAID = "paid", _("Pagada")
        FULFILLED = "fulfilled", _("Entregada")
        CANCELLED = "cancelled", _("Cancelada")
        REFUNDED = "refunded", _("Reembolsada")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders"
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    currency = models.CharField(max_length=3, default="mxn")
    total_mxn = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Referencia de la sesión de Stripe Checkout, para conciliar el webhook.
    stripe_session_id = models.CharField(max_length=255, blank=True, db_index=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"Orden #{self.pk} [{self.status}]"


class OrderItem(TimeStampedModel):
    class ItemType(models.TextChoices):
        COURSE = "course", _("Curso")
        PRODUCT = "product", _("Producto editorial")

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item_type = models.CharField(max_length=10, choices=ItemType.choices)
    # Referencia polimórfica ligera por id + tipo.
    course = models.ForeignKey(
        "academy.Course", on_delete=models.PROTECT, null=True, blank=True
    )
    product = models.ForeignKey(
        "publishing.Product", on_delete=models.PROTECT, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price_mxn = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Payment(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    stripe_payment_intent = models.CharField(max_length=255, blank=True, db_index=True)
    amount_mxn = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    succeeded = models.BooleanField(default=False)


class Refund(TimeStampedModel):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="refunds")
    amount_mxn = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reason = models.CharField(max_length=255, blank=True)


class ShippingDetail(TimeStampedModel):
    """Datos de envío para productos físicos."""

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="shipping")
    address = models.TextField()
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=12)
    country = models.CharField(max_length=2, default="MX")
    shipping_cost_mxn = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tracking_code = models.CharField(max_length=120, blank=True)


class ProcessedWebhookEvent(models.Model):
    """Garantiza idempotencia: cada event_id de Stripe se procesa una vez."""

    event_id = models.CharField(max_length=255, unique=True)
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.event_id
