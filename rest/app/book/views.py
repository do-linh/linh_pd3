from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import BookCategory, Book
from .serializers import BookCategorySerializer, BookSerializer

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class BookCategoryViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    serializer_class = BookCategorySerializer
    queryset = BookCategory.objects.all()

class BookViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    serializer_class = BookSerializer
    queryset = Book.objects.all()