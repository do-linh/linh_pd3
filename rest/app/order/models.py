from django.db import models
from django.db.models import Q, F
from django.conf import settings
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator
from ..book.models import Book
from . import OrderStatus, VoucherType,DiscountValueType
from decimal import Decimal
from functools import partial


class Address(models.Model):
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    company_name = models.CharField(max_length=256, blank=True)
    street_address_1 = models.CharField(max_length=256, blank=True)
    street_address_2 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    city_area = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = CountryField()
    country_area = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=10,blank=True, default="")

class VoucherQueryset(models.QuerySet):
    def active(self, date):
        return self.filter(
            Q(usage_limit__isnull=True) | Q(used__lt=F("usage_limit")),
            Q(end_date__isnull=True) | Q(end_date__gte=date),
            start_date__lte=date,
        )

    def expired(self, date):
        return self.filter(
            Q(used__gte=F("usage_limit")) | Q(end_date__lt=date), start_date__lt=date
        )

class Voucher(models.Model):
    type = models.CharField(
        max_length=20, choices=VoucherType.CHOICES, default=VoucherType.ENTIRE_ORDER
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=12, unique=True, db_index=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used = models.PositiveIntegerField(default=0, editable=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    # this field indicates if discount should be applied per order or
    # individually to every item
    apply_once_per_order = models.BooleanField(default=False)
    apply_once_per_customer = models.BooleanField(default=False)
    discount_value = models.IntegerField()

    objects = VoucherQueryset.as_manager()
    @property
    def is_free(self):
        return (
            self.discount_value == Decimal(100)
            and self.discount_value_type == DiscountValueType.PERCENTAGE
        )

    def get_discount(self):
        if self.discount_value_type == DiscountValueType.FIXED:
            discount_amount = Money(self.discount_value, settings.DEFAULT_CURRENCY)
            return partial(fixed_discount, discount=discount_amount)
        if self.discount_value_type == DiscountValueType.PERCENTAGE:
            return partial(percentage_discount, percentage=self.discount_value)
        raise NotImplementedError("Unknown discount type")

    
class Order(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=32, default=OrderStatus.UNFULFILLED, choices=OrderStatus.CHOICES
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="orders",
        on_delete=models.SET_NULL,
    )
    billing_address = models.ForeignKey(
        Address, related_name="+", editable=False, null=True, on_delete=models.SET_NULL
    )
    shipping_address = models.ForeignKey(
        Address, related_name="+", editable=False, null=True, on_delete=models.SET_NULL
    )
    user_email = models.EmailField(blank=True, default="")
    shipping_price = models.IntegerField(default=0,editable=False)
    total= models.IntegerField(default=0)
    voucher = models.ForeignKey(
        Voucher, blank=True, null=True, related_name="+", on_delete=models.SET_NULL
    )
    discount_amount = models.IntegerField(default=0)
    discount_name = models.CharField(max_length=255, blank=True, null=True)
    customer_note = models.TextField(blank=True, default="")

    def __iter__(self):
        return iter(self.lines.all())

    def __repr__(self):
        return "<Order #%r>" % (self.id,)

    def __str__(self):
        return "#%d" % (self.id,)

class OrderLine(models.Model):
    order = models.ForeignKey(
        Order, related_name="lines", editable=False, on_delete=models.CASCADE
    )
    product = models.ForeignKey(Book,related_name='order_lines',on_delete=models.SET_NULL,null=True, blank=True	)
    product_name = models.CharField(max_length=386)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    quantity_fulfilled = models.IntegerField(
        validators=[MinValueValidator(0)], default=0
    )
    unit_price=models.IntegerField()
    tax_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.0")
    )
