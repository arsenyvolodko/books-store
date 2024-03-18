from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField("Book", through="BookAuthor")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField("Book", through="BookCategory")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=150)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    page_count = models.IntegerField()
    published = models.DateTimeField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    long_description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10)
    authors = models.ManyToManyField('Author', through="BookAuthor")
    categories = models.ManyToManyField(Category, through="BookCategory")

    def __str__(self):
        return self.title


class BookCategory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book} - {self.category}"


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book} - {self.author}"


class CategoryHierarchy(models.Model):
    parent = models.ForeignKey("Category", on_delete=models.CASCADE)
    child = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="children")

    def __str__(self):
        return f"{self.parent} - {self.child}"
