from rest_framework import serializers
from .models import PaypalOrder, Payment


class PaypalOrderSerialzier(serializers.ModelSerializer):
    class Meta:
        model = PaypalOrder
        exclude  =  ["capture_url", 'token','links']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"