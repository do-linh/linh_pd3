from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .serializers import StockSerializer
from .models import Stock


class StockViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
