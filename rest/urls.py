"""rest_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest.app.profile.views import AuthorViewSet
from rest.app.book.views import BookReviewViewSet
router = DefaultRouter()
router.register(r'api/author',AuthorViewSet, basename='author')
router.register(r'api/review',BookReviewViewSet, basename='review')

urlpatterns = [
    path('api/user', include('rest.app.user.urls')),
    path('api/profile', include('rest.app.profile.urls')),
    path('api/book', include('rest.app.book.urls')),
    # path('api/order/', include('rest.app.order.urls')),
    path('api/checkout/', include("rest.app.checkout.urls")),
    path('api/stock/', include("rest.app.warehouse.urls")),
    path('api/payment/', include("rest.app.payment.urls")),
    path('paypal/', include("rest.app.payment.paypal_urls")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls
