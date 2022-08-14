#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 14:04:16 2019

@author: sambhav
"""
from django.conf.urls import url
from rest.app.book.views import BookCategoryViewSet, BookViewSet

urlpatterns = [
    url(r'/category/(?P<pk>\d+)$', BookCategoryViewSet.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
    url(r'/category', BookCategoryViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    url(r'/(?P<pk>\d+)$', BookViewSet.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
    url(r'', BookViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
]
