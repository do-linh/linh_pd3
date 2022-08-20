from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator
from ..book.models import Book
from . import OrderStatus
from decimal import Decimal
# # Create your models here.
# class OrderLine(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE, null=True)
#     ordered = models.BooleanField(default=False)
#     book = models.ForeignKey(Book, null=True, on_delete=models.CASCADE)
#     quantity = models.PositiveSmallIntegerField(default=1)
#     description = models.CharField(max_length=255, null=True, blank=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)
#     def total(self):
#         return self.book.pricebook * self.quantity

# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE, null=True)
#     lineOrder = models.ManyToManyField(OrderDetail)
#     total = models.BigIntegerField(null=True, blank=True)
#     ordered = models.BooleanField(default=False)
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)
#     def get_sub_total(self):
#         total = 0
#         for order_item in self.lineOrder.all():
#             total += order_item.total()
#         return total
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


class Voucher(models.Model):
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
