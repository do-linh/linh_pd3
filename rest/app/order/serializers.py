# from rest_framework.serializers import ModelSerializer
# from rest_framework import serializers
# from .models import Order, OrderDetail
# from ..user.serializers import UserSerializer

# class OrderDetailSER(ModelSerializer):
#     quantity = serializers.IntegerField(min_value=0)
#     class Meta:
#         model = OrderDetail
#         fields = '__all__'

# class OrderSER(ModelSerializer):
#     total = serializers.IntegerField(read_only=True)
#     # lineOrder = OrderDetailSER()
#     class Meta:
#         model = Order
#         fields = '__all__'