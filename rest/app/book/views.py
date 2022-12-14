
from rest_framework import viewsets, status
from .models import BookCategory, Book,UserFavoriteList
from .serializers import BookCategorySerializer, BookSerializer,UserFavoriteListSER
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class BookCategoryViewSet(viewsets.ModelViewSet):

    permission_classes = (AllowAny,)
    authentication_class = JSONWebTokenAuthentication

    serializer_class = BookCategorySerializer
    queryset = BookCategory.objects.all()

class BookViewSet(viewsets.ModelViewSet):

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = (AllowAny,)
    authentication_class = JSONWebTokenAuthentication

    filter_backends  = (SearchFilter,)
    search_fields = ('namebook','id_sach', "id_category__name_category", 'author')
    parser_classes = (MultiPartParser, FormParser,JSONParser)


class UserFavoriteListViewSet(viewsets.ModelViewSet):
    serializer_class = UserFavoriteListSER 
    queryset = UserFavoriteList.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
