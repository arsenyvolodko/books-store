from django.urls import path
from books import views

urlpatterns = [
    path('get_books/', views.get_books, name='get_books'),
    path('get_cats_and_books/', views.get_cats_and_books, name='get_cats_and_books'),
    path('get_book/<int:book_id>', views.get_book, name='get_book'),
]
