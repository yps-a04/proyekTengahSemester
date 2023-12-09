from django.db import models

# Create your models here.


class Book (models.Model):
    title = models.TextField(("title"), max_length=255, null=True, blank=True)
    author = models.TextField(
        ("author"), max_length=255, null=True, blank=True)
    average_rating = models.FloatField(
        ("average rating"), null=True, blank=True)
    isbn = models.TextField(("isbn"), max_length=150, null=True, blank=True)
    isbn13 = models.TextField(
        ("isbn 13"), max_length=150, null=True, blank=True)
    language_code = models.TextField(
        ("language code"), max_length=10, null=True, blank=True)
    num_pages = models.IntegerField(("number of pages"), null=True, blank=True)
    rating_count = models.BigIntegerField(
        ("rating count"), null=True, blank=True)
    text_review_count = models.BigIntegerField(
        ("text review count"), null=True, blank=True)
    publication_date = models.DateField(
        ("publication date"), auto_now=True, null=True, blank=True)
    publisher = models.TextField(
        ("publisher"), max_length=150, null=True, blank=True)
