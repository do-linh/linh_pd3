from rest_framework import serializers
from rest_framework.serializers import StringRelatedField
from .models import Order, OrderLine, Address

from ...serializers import StringSerializer

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['id']

class OrderLineSerializer(serializers.ModelSerializer):
    book  = StringSerializer()
    class Meta:
        model = OrderLine
        fields = ['book' , 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(many=True)
    billing_address = AddressSerializer()
    shipping_address = AddressSerializer()
    # sub_total = serializers.CharField(source='sub_total', read_only=True)
    class Meta:
       
        
        model = Order
        # fields = ['lines', 'created_date', 'shipping_price', 'total', 'customer_note', '']
        exclude = ['voucher','discount_amount', 'discount_name']