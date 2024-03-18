from django.db import models


# Create your models here.
class Feedback(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=150)
    comment = models.TextField()
    phone = models.CharField(max_length=13)
