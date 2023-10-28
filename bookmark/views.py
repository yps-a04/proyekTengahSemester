from django.shortcuts import render
from main.models import Book
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from bookmark.models import Bookmark
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def show_bookmark(request, key):
    if request.user.username == key:  
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
    return HttpResponse("cannot access")

def delete_bookmark(request, key):
    book = get_object_or_404(Book, pk=key)
    if request.method == 'POST':
        user = request.user
        try:
            existing_bookmark = Bookmark.objects.get(user=user, book=book)
            existing_bookmark.delete()
            return JsonResponse({'status': 'unbookmarked'})
        except Bookmark.DoesNotExist:
            new_bookmark = Bookmark(user=user, book=book)
            new_bookmark.save()
            return JsonResponse({'status': 'bookmarked'})
# Create your views here.
