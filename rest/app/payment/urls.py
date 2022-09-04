from django.urls import path
from .views import CaptureOrderAPIView

urlpatterns = [
    path("capture/", CaptureOrderAPIView.as_view())
]