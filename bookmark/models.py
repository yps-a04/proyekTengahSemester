from django.db import models
from django.contrib.auth.models import User
from book.models import Book

class Bookmark(models.Model):
    user = models.ForeignKey(
        User, related_name='bookmarked', on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, related_name='bookmarked', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username