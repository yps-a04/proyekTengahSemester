from django.db import models
from main.models import *
from book_details.models import *
# Create your models here.
class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(("author"), max_length=255)
