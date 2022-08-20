#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 19:10:16 2019

@author: sambhav
"""

from django.conf.urls import url
from django.urls import path
from .views import UserProfileView, UserFavoriteListAPIView



urlpatterns = [
    path('<uuid:profile_id>/favorite',UserFavoriteListAPIView.as_view()),
    url(r'', UserProfileView.as_view()),
    ]
