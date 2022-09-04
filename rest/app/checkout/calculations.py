from typing import Iterable
from .models import Checkout, CheckoutLine
from ..order.models import Voucher
from django.shortcuts import get_object_or_404

def calculate_checkout_line_total(line: "CheckoutLine", discounts):
    amount = line.quantity * line.book.get_price(discounts or [])
    return amount
def checkout_line_total(
    *, line: "CheckoutLine", discounts = None
) :
    """Return the total price of provided line, taxes included.

    eg:     sale: Voucher
    product_ids: Union[List[int], Set[int]]

    """
    calculated_line_total = calculate_checkout_line_total(
        line, discounts or []
    )
    return calculated_line_total

def calculate_checkout_total(checkout:"Checkout", checkout_lines:Iterable[CheckoutLine], discount_value):

    total = sum([ line.calculate_checkout_line_total() for line in checkout_lines])

    return total - discount_value
