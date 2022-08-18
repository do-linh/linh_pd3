from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


from .serializers import OrderDetailSER,OrderSER
from .models import OrderDetail, Order

class OrderDetailViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSER

    def _list(self,request):
        serializer = OrderDetailSER(self.queryset,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def _retrieve(self,request, pk):
        order_detail = get_object_or_404(self.queryset, pk=pk)
        serializer = OrderDetailSER(order_detail)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        serializer = OrderDetailSER(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def delete(self,request,pk):
        order_detail = get_object_or_404(self.queryset, pk=pk)
        order_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSER


    