from django.urls import path
from book_details.views import *

app_name = 'book_details'

urlpatterns = [
    path('book-detail/<int:key>', show_book_detail, name='show_book_detail'),
]
