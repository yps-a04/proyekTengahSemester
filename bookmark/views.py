from django.shortcuts import render
from main.models import Book
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from book_details.models import Bookmark
from django.contrib.auth.models import User

def show_bookmark(request, key):
    username = key
    user = User.objects.get(username=username)
    book = user.bookmarked.values('book')
    p = Paginator(book, 50)
    page = request.GET.get('page')

    books = p.get_page(page)
    context = {
        'books': books,
        'username' : username,
    }
    return render(request, "bookmark.html", context)

# Create your views here.
