from datetime import datetime

import pytz
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books_store.settings import TIME_ZONE
from .serializers import BookSerializer, CategoriesAndBooks
from .models import Book, Category

# Create your views here.

BOOKS_PER_PAGE = 50


def get_range_by_page(page_num: int):
    return range((page_num - 1) * BOOKS_PER_PAGE, page_num * BOOKS_PER_PAGE + 1)


def get_books_util(**kwargs):
    range_ = kwargs.pop('range_', None)
    # books = Book.objects.filter(**kwargs).all()
    books = Book.objects.filter(**kwargs).all()
    if range_:
        lb, rb = range_[0], range_[-1]
        books = books[lb: rb]
    return books


def get_date(date_str: str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').astimezone(tz=pytz.timezone(TIME_ZONE))
    except ValueError:
        return None


@swagger_auto_schema(
    operation_description="Возвращает книги с возможностью фильтрации по категории и пагинации",
    method='get',
    manual_parameters=[
        openapi.Parameter('category', openapi.IN_QUERY, description="Категория возвращаемых книг",
                          type=openapi.TYPE_STRING,
                          required=False),
        openapi.Parameter('author', openapi.IN_QUERY, description="Автор книги",
                          type=openapi.TYPE_STRING,
                          required=False),
        openapi.Parameter('status', openapi.IN_QUERY, description="Статус книги",
                          type=openapi.TYPE_STRING,
                          required=False),
        openapi.Parameter('title', openapi.IN_QUERY, description="Название книги",
                          type=openapi.TYPE_STRING,
                          required=False),
        openapi.Parameter('since', openapi.IN_QUERY, description="Дата публикации книги не ранее",
                          type=openapi.TYPE_STRING,
                          required=False),
        openapi.Parameter('until', openapi.IN_QUERY, description="Дата публикации книги не позднее (формат: YYYY-MM-DD)",
                          type=openapi.TYPE_STRING,
                          required=False),
        openapi.Parameter('page', openapi.IN_QUERY, description="Номер страницы (на странице 50 записей)",
                          type=openapi.TYPE_INTEGER,
                          required=False),
    ],
    responses={200: BookSerializer(many=True),
               404: 'Invalid page number format'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_books(request):
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except ValueError:
        return Response({'error': 'Invalid page number'}, status=status.HTTP_404_NOT_FOUND)
    data = {
        'range_': get_range_by_page(page),
    }
    if category := request.GET.get('category'):
        data['bookcategory__category__name'] = category
    if author := request.GET.get('author'):
        data['bookauthor__author__name'] = author
    if book_status := request.GET.get('status'):
        data['status__exact'] = book_status
    if title := request.GET.get('title'):
        data['title__exact'] = title
    if since := request.GET.get('since'):
        data['published__gte'] = get_date(since)
    if until := request.GET.get('until'):
        data['published__lte'] = get_date(until)
    books = get_books_util(**data)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    operation_description="Возвращает книги указанной категории, подкатегории данной категории на 1 уровень вниз, а также книги данных подкатегорий",
    method='get',
    manual_parameters=[
        openapi.Parameter('category', openapi.IN_QUERY,
                          description="Категория, книги которой возвращаются и все книги подкатегорий данной категории",
                          type=openapi.TYPE_STRING,
                          required=True),
    ],
    responses={200: CategoriesAndBooks,
               400: 'No category specified'},
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


@swagger_auto_schema(
    operation_description="Возвращает информацию о книге по её ID",
    method='get',
    manual_parameters=[
        openapi.Parameter('book_id', openapi.IN_PATH, description="ID книги", type=openapi.TYPE_INTEGER,
                          required=True),
    ],
    responses={200: BookSerializer,
               404: 'Invalid book_id'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book(request, book_id: int):
    book = get_object_or_404(Book, pk=book_id)
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)
