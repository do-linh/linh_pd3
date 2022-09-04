from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import APIException
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import PaypalOrder, Payment
from .paypal import capture_a_paypal_order
from ..order.serializers import OrderSerializer

class SuccessPaypalCheckout(views.APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        paypal_token = request.GET.get('token')
        if paypal_token:
            paypal_order = get_object_or_404(PaypalOrder, token=paypal_token)
            try:
                payment = Payment.objects.get(paypal_order__checkout=paypal_token)
                if payment:
                    return Response({'message': "Already exists"}, status=status.HTTP_200_OK)
            except:
                pass
            order=  capture_a_paypal_order(paypal_order)
            serializer= OrderSerializer(order)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class CaptureOrderAPIView(views.APIView):
    """return order after capturing success"""
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        paypal_token = request.data.get('token')
        
        if paypal_token:
            paypal_order = get_object_or_404(PaypalOrder, token=paypal_token)
            # try:
            #     payment = Payment.objects.get(paypal_order__token=paypal_token)
            #     if payment:
            #         return Response({'message': "Already exists"}, status=status.HTTP_200_OK)
            # except:
            #     pass
            try:
                capture_a_paypal_order(paypal_order)
            except Exception as err:
                raise APIException(err) 

            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)