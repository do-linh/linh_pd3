from ..order.models import Voucher
from .models import Checkout

from django.utils import timezone

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