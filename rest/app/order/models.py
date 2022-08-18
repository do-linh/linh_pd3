from django.db import models
from django.conf import settings
from ..book.models import Book

# Create your models here.
class OrderDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    ordered = models.BooleanField(default=False)
    book = models.ForeignKey(Book, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def total(self):
        return self.book.pricebook * self.quantity

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    lineOrder = models.ManyToManyField(OrderDetail)
    total = models.BigIntegerField(null=True, blank=True)
    ordered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def get_sub_total(self):
        total = 0
        for order_item in self.lineOrder.all():
            total += order_item.total()
        return total