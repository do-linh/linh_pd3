from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import viewsets, status,views, generics
from .models import BookCategory, Book,UserFavoriteList, BookReview
from .serializers import BookCategorySerializer, BookReviewSerializer, BookSerializer,UserFavoriteListSER

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
    

class BookReviewAPIView(views.APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class= BookReviewSerializer
    queryset= BookReview.objects.all()

    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        queryset = BookReview.objects.filter(book=book)
        serializer = BookReviewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, book_id):
        print(request.user, type(request.user))
        # request.data['user'] = user
        serializer = BookReviewSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.perform_create(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class BookReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = BookReviewSerializer
    queryset= BookReview.objects.all()
