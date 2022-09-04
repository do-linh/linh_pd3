from .views import CheckoutAPIView,CheckoutLineAddAPIView, PaypalOrderAdd

from django.urls import path

urlpatterns = [
    path('', CheckoutAPIView.as_view()),
    path('<int:checkout_id>/add_lines', CheckoutLineAddAPIView.as_view()),
    path('<int:checkout_id>/paypal_checkout', PaypalOrderAdd.as_view()),
]