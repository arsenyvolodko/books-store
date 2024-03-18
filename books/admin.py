from django.contrib import admin

from books.forms import CategoryHierarchyForm
# Register your models here.
from books.models import Author, Book, BookAuthor, BookCategory, Category, CategoryHierarchy


@admin.register(CategoryHierarchy)
class CategoryHierarchyAdmin(admin.ModelAdmin):
    form = CategoryHierarchyForm
