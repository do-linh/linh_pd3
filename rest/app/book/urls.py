
from django.urls import path
from django.conf.urls import url
from rest.app.book.views import BookCategoryViewSet, BookViewSet, BookReviewAPIView, BookReviewViewSet



urlpatterns = [
    path('<int:book_id>/review', BookReviewAPIView.as_view() ), 

    url(r'category/(?P<pk>\d+)$', BookCategoryViewSet.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
    url(r'category', BookCategoryViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    url(r'(?P<pk>\d+)$', BookViewSet.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
    url(r'', BookViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    
]
