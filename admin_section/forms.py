from django.forms import ModelForm
from main.models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "average_rating", "isbn", "isbn13",
                  "language_code", "num_pages", "rating_count", "text_review_count", "publisher"]