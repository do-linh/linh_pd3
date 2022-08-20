from rest_framework import serializers
from .models import BookCategory, Book,FavoriteList

class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value
class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(required=False)
    class Meta:
        model = Book
        fields = '__all__'

class UserFavoriteListSER(serializers.ModelSerializer):

    class Meta:
        model = FavoriteList
        fields = '__all__'
    def create(self, validated_data):
        books = validated_data.pop('books')
        fav_list, created = FavoriteList.objects.update_or_create(**validated_data)
        if not created:
            fav_list.books.remove()
        for book in books:
            print('add book:', book)
            print(fav_list.books.add(book))
        return fav_list
