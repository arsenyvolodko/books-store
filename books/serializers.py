from rest_framework import serializers
from .models import Book, Author, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_authors(self, obj):
        return [author.name for author in obj.authors.all()]

    def get_categories(self, obj):
        return [category.name for category in obj.categories.all()]
