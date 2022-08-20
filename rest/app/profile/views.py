#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 17:25:00 2019

@author: sambhav
"""
from rest_framework import status,viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from rest.app.user.serializers import UserRegistrationSerializer
from rest.app.profile.models import UserProfile
from rest.app.book.models import FavoriteList
from ..book.serializers import BookSerializer, UserFavoriteListSER

from .models import Author
from .serializers import AuthorSER


class UserProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'id': user_profile.pk, 
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'phone_number': user_profile.phone_number,
                    'age': user_profile.age,
                    'gender': user_profile.gender,
                    'role': user_profile.role,
                    'user_id': user_profile.user.id
                }]
            }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)

class UserFavoriteListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request, profile_id, *arg, **kwargs):
        profile = get_object_or_404(UserProfile, pk=profile_id)
        queryset, _ = FavoriteList.objects.get_or_create(profile=profile)
        books = queryset.books.all()
        books_SER = BookSerializer(books,many=True)
        return Response(books_SER.data, status=status.HTTP_200_OK)
        # return Response(books_SER.data,status=status.HTTP_400_BAD_REQUEST)
    def post(self, request,profile_id):
        favorite_SER = UserFavoriteListSER(data=request.data)
        favorite_SER.is_valid(raise_exception=True)
        fav_list = favorite_SER.create(validated_data=favorite_SER.validated_data)
        return Response(UserFavoriteListSER(fav_list).data,status=status.HTTP_201_CREATED)


class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = AuthorSER
    queryset = Author.objects.all()
    parser_classes = (MultiPartParser, FormParser,JSONParser)
