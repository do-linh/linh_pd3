
from ..book.models import Book
from ..warehouse.models import Stock
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException

class InsufficientStock(APIException):
    status_code = 400
    default_code = "insuffcient_stock"
    default_detail = ""
def check_stock_quantity(book: "Book", quantity: int):
    """Validate if there is stock available for given book .
    If so - returns None. If there is less stock then required raise InsufficientStock
    exception.
    """
    
    try:
        stock =Stock.objects.get(product=book)
    except:
        stock = None
    print("Debug: Stock", stock)
    if not stock:
        raise InsufficientStock(f'Product{book.get_display()} is out of stock')
    if quantity > stock.quantity:
        return InsufficientStock(f'Product{book.get_display()} is out of stock')
        