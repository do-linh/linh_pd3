from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# from .views import OrderDetailViewSet,OrderViewSet
# router.register(r'detail',OrderDetailViewSet,basename='order_detail' )
# router.register(r'',OrderViewSet,basename='order' )


urlpatterns = router.urls
