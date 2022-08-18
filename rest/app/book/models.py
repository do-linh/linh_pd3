from django.db import models
from ..user.models import User
from ..profile.models import UserProfile
# Create your models here.

class BookCategory(models.Model):
    id_category = models.AutoField(primary_key=True)
    name_category = models.CharField(max_length=255)

class Book(models.Model):
    id_sach = models.AutoField(primary_key=True)
    id_category = models.ForeignKey(BookCategory, to_field='id_category', on_delete=models.CASCADE)
    namebook = models.CharField(max_length=500)
    author = models.CharField(max_length=225)
    categorybook = models.TextField()
    pricebook = models.BigIntegerField()
    status = models.TextField()
    image = models.ImageField(upload_to='item/', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(auto_now=True)

class UserFavoriteList(models.Model): #deprecated
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, null=True, blank=True)
    created_date =  models.DateTimeField(auto_now_add=True)
    updated_date =  models.DateTimeField(auto_now=True)

class FavoriteList(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)


