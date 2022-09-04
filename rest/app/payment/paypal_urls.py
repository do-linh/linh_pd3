from .views import *

from django.urls import path
from .views import SuccessPaypalCheckout

urlpatterns = [
    path('checkout',SuccessPaypalCheckout.as_view())
]