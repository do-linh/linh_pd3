from ..order.models import Voucher
from .models import Checkout, CheckoutLine
from ..warehouse.availabiltity import check_stock_quantity
from ..order.models import Order, OrderLine
from ..payment.models import Payment
from django.db.models import F

from django.utils import timezone
def increase_voucher_usage(voucher: "Voucher") -> None:
    """Increase voucher uses by 1."""
    voucher.used = F("used") + 1
    voucher.save(update_fields=["used"])

def decrease_voucher_usage(voucher: "Voucher") -> None:
    """Decrease voucher uses by 1."""
    voucher.used = F("used") - 1
    voucher.save(update_fields=["used"])


def get_voucher_for_checkout(
    checkout: Checkout, vouchers=None, with_lock: bool = False):
    """Return voucher with voucher code saved in checkout if active or None."""
    if checkout.voucher_code is not None:
        if vouchers is None:
            vouchers = Voucher.objects.active(date=timezone.now())
        try:
            qs = vouchers
            if with_lock:
                qs = vouchers.select_for_update()
            return qs.get(code=checkout.voucher_code)
        except Voucher.DoesNotExist:
            return None
    return None
def _create_line_for_order(checkout_line: "CheckoutLine"):
    quantity = checkout_line.quantity
    book = checkout_line.book
    check_stock_quantity(book, quantity)
    
    line = OrderLine(
        book_name = str(book),
        book = book,
        quantity=quantity,
        unit_price=book.pricebook
    )
    return line


def _prepare_order_data(checkout: "Checkout", payment: "Payment"):
    """raise InsufficientStock"""
    order_data = {
        "user": checkout.user,
        "billing_address": payment.get_billing_address(), 
        "shipping_address": checkout.shipping_address,
        "shipping_price" : checkout.shipping_price, 
        "total" : checkout.get_checkout_total() + checkout.shipping_price
    }
    order_data['lines'] = [
        _create_line_for_order(line) for line in list(checkout)
    ]

    return order_data

def _create_order(checkout: "Checkout", order_data:dict):
    order_lines = order_data.pop('lines')
    order = Order.objects.create(**order_data)

    for line in order_lines :
        line.order_id = order.pk
    
    order_lines = OrderLine.objects.bulk_create(order_lines)
    checkout.payments.update(order=order)

    order.save()

    return order


def complete_checkout(checkout: "Checkout", payment: "Payment"):
    """create an order correctspdodng  checkout and payment, then delete the checkout"""
    order_data = _prepare_order_data(checkout, payment)
    order = None
    order = _create_order(checkout, order_data)
    checkout.delete()
    return order

