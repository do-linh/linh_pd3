from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

from ..order.models import Address
from ..book.models import Book

class Checkout(models.Model):
    """A shopping checkout."""

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="checkouts",
        on_delete=models.CASCADE,
    )
    email = models.EmailField()
    quantity = models.PositiveIntegerField(default=0)
    billing_address = models.ForeignKey(
        Address, related_name="+", editable=False, null=True, on_delete=models.SET_NULL
    )
    shipping_address = models.ForeignKey(
        Address, related_name="+", editable=False, null=True, on_delete=models.SET_NULL
    )

    note = models.TextField(blank=True, default="")

    discount = models.IntegerField(
        default=0,
    )
    discount_name = models.CharField(max_length=255, blank=True, null=True)

    voucher_code = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        ordering = ("-updated_date", "pk")
        # permissions = (
        # )

    def __repr__(self):
        return "Checkout(quantity=%s)" % (self.quantity,)

    def __iter__(self):
        return iter(self.lines.all())

    def get_customer_email(self) -> str:
        return self.user.email if self.user else self.email


    # def get_line(self, variant):
    #     """Return a line matching the given book and data if any."""
    #     matching_lines = (line for line in self if line.variant.pk == variant.pk)
    #     return next(matching_lines, None)

class CheckoutLine(models.Model):
    """A single checkout line.

    Multiple lines in the same checkout can refer to the same product variant if
    their `data` field is different.
    """

    checkout = models.ForeignKey(
        Checkout, related_name="lines", on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book, related_name="+", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])