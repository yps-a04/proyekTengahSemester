from django.urls import path
from main.views import *
app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('book-list/', show_book_list, name='show_book_list'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('search/', search, name='search'),
    path('sort-books/', sort_books, name='sort_books'),



    path('b/<str:key>', bookmark, name='bookmark'),

]
