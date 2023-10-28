from django.shortcuts import render
from main.models import Book
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from bookmark.models import Bookmark
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def show_bookmark(request, key):
    username = key
    user = User.objects.get(username=username)
    book = user.bookmarked.select_related('book')

    p = Paginator(book, 20)
    page = request.GET.get('page')

    books = p.get_page(page)
    context = {
        'books': books,
        'username' : username,
    }
    return render(request, "bookmark.html", context)

def delete_bookmark(request, key):
    book = get_object_or_404(Book, pk=key)
    existing_bookmark = Bookmark.objects.get(user=request.user, book=book)
    existing_bookmark.delete()
    return HttpResponseRedirect(reverse('bookmark:show_bookmark', args=[request.user.username]))
# Create your views here.
