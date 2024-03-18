from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import BookSerializer
from .models import Book, Category

# Create your views here.

BOOKS_PER_PAGE = 50


def get_range_by_page(page_num: int):
    return range((page_num - 1) * BOOKS_PER_PAGE, page_num * BOOKS_PER_PAGE + 1)


def get_books_util(**kwargs):
    if category := kwargs.get('category'):
        books = Book.objects.filter(bookcategory__category__name=category).all()
    else:
        books = Book.objects.all()

    if range_ := kwargs.get('range_'):
        lb, rb = range_[0], range_[-1]
        books = books[lb: rb]
    return books


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('category', openapi.IN_QUERY, description="Категория возвращаемых книг",
                          type=openapi.TYPE_STRING,
                          required=False),
        openapi.Parameter('page', openapi.IN_QUERY, description="Номер страницы (на странице 50 записей)",
                          type=openapi.TYPE_INTEGER,
                          required=False),
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_books(request):
    category = request.GET.get('category')
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except ValueError:
        return Response({'error': 'Invalid page number'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'range_': get_range_by_page(page),
        'category': category
    }
    books = get_books_util(**data)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('category', openapi.IN_QUERY,
                          description="Категория, книги которой возвращаются и все книги подкатегорий данной категории",
                          type=openapi.TYPE_STRING,
                          required=True),
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cats_and_books(request):
    category = request.GET.get('category')
    if not category:
        return Response({'error': 'No category'}, status=status.HTTP_400_BAD_REQUEST)
    cur_books = get_books_util(category=category)
    subcategories = Category.objects.filter(children__parent__name__exact=category).all()
    res = {
        'books': BookSerializer(cur_books, many=True).data,
        'subcategories': {
            cat.name: {
                'books': BookSerializer(get_books_util(category=cat), many=True).data
            } for cat in subcategories
        }
    }
    return Response(res, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book(request, book_id: int):
    book = get_object_or_404(Book, pk=book_id)
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)
