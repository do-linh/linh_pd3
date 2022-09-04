from django.db import models
from django.db.models import F, Sum
from ..book.models import Book
# Create your models here.

class Stock(models.Model):
    warehouse = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(
        Book, null=False, on_delete=models.CASCADE, related_name="stocks"
    )
    quantity = models.PositiveIntegerField(default=0)


    class Meta:
        ordering = ("pk",)

    def increase_stock(self, quantity: int, commit: bool = True):
        """Return given quantity of product to a stock."""
        self.quantity = F("quantity") + quantity
        if commit:
            self.save(update_fields=["quantity"])

    def decrease_stock(self, quantity: int, commit: bool = True):
        self.quantity = F("quantity") - quantity
        if commit:
            self.save(update_fields=["quantity"])