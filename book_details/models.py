from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Book (models.Model):
    title = models.CharField(("title"), max_length=255)
    author = models.CharField(("author"), max_length=255)
    average_rating = models.FloatField(("average rating"))
    isbn = models.CharField(("isbn"), max_length=150)
    isbn13 = models.CharField(("isbn 13"), max_length=150)
    language_code = models.CharField(("language code"), max_length=10)
    num_pages = models.IntegerField(("number of pages"))
    rating_count = models.BigIntegerField(("rating count"))
    text_review_count = models.BigIntegerField(("text review count"))
    publication_date = models.DateField(("publication date"), auto_now=True)
    publisher = models.CharField(("publisher"), max_length=150)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    review = models.TextField()

class Bookmark(models.Model):
    user = models.ForeignKey(User, related_name='bookmarked', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='bookmarked', on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username