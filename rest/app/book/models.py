from django.db import models
from django.utils.numberformat import format
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from ..user.models import User
from ..profile.models import UserProfile
from ..profile.models import Author
# Create your models here.

class BookCategory(models.Model):
    id_category = models.AutoField(primary_key=True)
    name_category = models.CharField(max_length=255)

class Book(models.Model):
    id_sach = models.AutoField(primary_key=True)
    id_category = models.ForeignKey(BookCategory, to_field='id_category', on_delete=models.CASCADE)
    namebook = models.CharField(max_length=500)
    author = models.CharField(max_length=225)
    book_author = models.ForeignKey(Author,on_delete=models.CASCADE, null=True, blank=True)
    categorybook = models.TextField()
    pricebook = models.BigIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='item/', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(auto_now=True)
    is_trend = models.BooleanField(default=False)

    def get_price_for_paypal(self):
        price = self.pricebook / 20000
        return "%.2f" % round(price, 2)
    def get_display(self):
        return f"{self.namebook} - {self.author} ( {format(self.pricebook, decimal_sep=',', decimal_pos=0, grouping=3, thousand_sep=' ', force_grouping=True)} VND) "
    
    def get_description(self):
        return self.description
    
    def __str__(self) -> str:
        return self.namebook


class BookReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rate = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    review = models.TextField(null=True)
    is_negative = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)



class UserFavoriteList(models.Model): #deprecated
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    created_date =  models.DateTimeField(auto_now_add=True)
    updated_date =  models.DateTimeField(auto_now=True)

class FavoriteList(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)


