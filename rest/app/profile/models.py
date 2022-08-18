#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:04:16 2019

@author: sambhav
"""

import uuid
from django.db import models
from rest.app.user.models import User


class UserProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    phone_number = models.CharField(
        max_length=10, unique=True, null=False, blank=False)
    age = models.PositiveIntegerField(null=False, blank=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    ROLE_CHOICES = (
        (0, 'Admin'),
        (1, 'Customer'),
    )
    role = models.BigIntegerField(choices=ROLE_CHOICES, default=1, editable=False)

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "profile"

class Author(models.Model):
    author_id = models.BigAutoField(primary_key=True)
    author_name = models.CharField(max_length=255)
    author_avatar = models.ImageField(upload_to='author/', null=True, blank=True)
    author_description = models.TextField(null=True, blank=True	)
    author_dob = models.DateTimeField(null=True, blank=True	)