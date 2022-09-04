from .serializers import CheckoutLineSerializer, WriteCheckoutSerializer,ReadCheckoutSerializer
from rest_framework import viewsets, generics,views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Checkout
from ..payment.paypal import create_an_paypal_order
from ..payment.models import PaypalOrder
from ..payment.serializers import PaypalOrderSerialzier

def check_lines_quantity(books, quantities ):
    return

class CheckoutAPIView(views.APIView):
    permission_classes =  (IsAuthenticated,)
    def get_serializer(self, *arg, **kwargs):
        if self.request.method == 'POST':
            return WriteCheckoutSerializer(**kwargs)
        return ReadCheckoutSerializer(**kwargs)
    def get(self,request):
        user = request.user
        queryset = Checkout.objects.get(user=user)
        serializer = ReadCheckoutSerializer(queryset)
        return Response(serializer.data)
    def post(self, request):
        checkout_ser = self.get_serializer(data=request.data)
        checkout_ser.is_valid(raise_exception=True)
        checkout_ser.request= request
        ins = checkout_ser.save()
        checkout = ReadCheckoutSerializer(ins)
        return Response(checkout.data, status=status.HTTP_201_CREATED)


class CheckoutLineAddAPIView(views.APIView):
    permission_classes =  (IsAuthenticated,)
    
    def patch(self,request,checkout_id):
        checkout = get_object_or_404(Checkout, pk=checkout_id)
        checkout_ser = WriteCheckoutSerializer(checkout, data=request.data, partial=True)
        checkout_ser.is_valid(raise_exception=True)
        checkout_ser.perform_update(instance=checkout)

        return Response({}, status=status.HTTP_201_CREATED)

class PaypalOrderAdd(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, checkout_id):
        checkout = get_object_or_404(Checkout, pk=checkout_id)
        try:
            paypal_order = create_an_paypal_order(checkout)
            data = PaypalOrder.objects.create(**paypal_order)
            serializer = PaypalOrderSerialzier(data)
            return Response(serializer.data,status=status.HTTP_201_CREATED) 
        except Exception as err:
            return Response({"error":err.__repr__()}, status=status.HTTP_400_BAD_REQUEST)

