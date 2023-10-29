from django.urls import path
from book_details.views import *

app_name = 'book_details'

urlpatterns = [
    path('book-detail/<int:key>', show_book_detail, name='show_book_detail'),
    path('add-review/<int:key>', add_review, name='add_review'),
    path('get-reviews-json/', get_reviews_json, name='get_reviews_json'),
    path('add-review-ajax/', add_review_ajax, name='add_review_ajax'),
]
