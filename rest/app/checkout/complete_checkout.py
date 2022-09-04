from .models import Checkout, CheckoutLine, NotApplicable
from .utils import get_voucher_for_checkout, increase_voucher_usage, checkout_total
from ..order.models import OrderLine
from ..warehouse.availabiltity import check_stock_quantity
from typing import Iterable, List, Optional, Tuple
from decimal import Decimal
def _process_user_data_for_order(checkout: Checkout):
    """Fetch, process and return shipping data from checkout."""
    billing_address = checkout.billing_address
    
    return {
        "user": checkout.user,
        "user_email": checkout.get_customer_email(),
        "billing_address": billing_address,
        "customer_note": checkout.note,
    }
def _get_voucher_data_for_order(checkout: Checkout) -> dict:
    """Fetch, process and return voucher/discount data from checkout.

    Careful! It should be called inside a transaction.

    :raises NotApplicable: When the voucher is not applicable in the current checkout.
    """
    voucher = get_voucher_for_checkout(checkout, with_lock=True)

    if checkout.voucher_code and not voucher:
        msg = "Voucher expired in meantime. Order placement aborted."
        return NotApplicable(msg)

    if not voucher:
        return {}

    increase_voucher_usage(voucher)
    return {
        "voucher": voucher,
        "discount": checkout.discount,
        "discount_name": checkout.discount_name,
    }
def _create_line_for_order(checkout_line: "CheckoutLine", discounts) -> OrderLine:
    """Create a line for the given order.

    :raises InsufficientStock: when there is not enough items in stock for this variant.
    """

    quantity = checkout_line.quantity
    book = checkout_line.book
    check_stock_quantity(book, quantity)

    product_name = book.namebook

    total_line_price = checkout_line.calculate_checkout_line_total(discounts)
    unit_price = total_line_price / checkout_line.quantity
    tax_rate = Decimal("0.0")
    # The condition will return False when unit_price.gross is 0.0
    if not isinstance(unit_price, Decimal) and unit_price.gross:
        tax_rate = unit_price.tax / unit_price.net

    line = OrderLine(
        product_name=product_name,
        quantity=quantity,
        book=book,
        unit_price=unit_price,  # type: ignore
        tax_rate=tax_rate,
    )

    return line
