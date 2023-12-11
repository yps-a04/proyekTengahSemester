from django.db import models
from django.contrib.auth.models import User
from book.models import Book

# Create your models here.


class Review(models.Model):
    user = models.ForeignKey(
        User, related_name='reviewed', on_delete=models.CASCADE, default=None)
    book = models.ForeignKey(
        Book, related_name='reviewed', on_delete=models.CASCADE, default=None)
    review = models.TextField(null=True, blank=True, default=None)
    title = models.TextField(null=True, blank=True, default=None)
