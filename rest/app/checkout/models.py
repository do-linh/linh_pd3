from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from operator import attrgetter

from ..order.models import Address
from ..book.models import Book

from rest_framework.exceptions import APIException
class NotApplicable(APIException):
    status_code = 400
    default_code = 'not_applicable'
    default_detail = ''
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
    shipping_price = models.IntegerField(default=30000)
    
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

    def get_last_payment(self):
        return max(self.payments.all(), default=None, key=attrgetter("pk"))

    def get_checkout_total(self):
        sum = 0 
        for line in self :
            sum += line.calculate_checkout_line_total()
        return sum 
    def get_paypal_total_amout(self):
        return "%.2f" % round(self.get_checkout_total() / 20000, 2)


  
    

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

    def calculate_checkout_line_total(self, discount: int=0):
        return (self.quantity * self.book.pricebook) - discount