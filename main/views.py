from django.shortcuts import render, redirect
from main.models import Book
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import LoginForm, SignUpForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from bookmark.models import Bookmark
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
# Create your views here.


def show_main(request):

    # set pagination 50/page
    p = Paginator(Book.objects.all(), 20)
    page = request.GET.get('page')

    top5 = Book.objects.all()[:5]
    books = p.get_page(page)
    print(top5)

    bookmarks = None
    if request.user.is_authenticated:
        bookmarks = request.user.bookmarked.select_related('book')

    b = [] 
    for book in bookmarks:
        b.append(book.book)

    context = {
        'books': books,
        'top5': top5,
        'bookmarks' : b
    }

    return render(request, "main.html", context)

def bookmark(request, key):
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


def register(request):
    form = SignUpForm()
    context = {'form': form}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your account has been successfully created!')
            return redirect('main:login')
        else:
            messages.info(
                request, "Register Failed. Make sure your password is strong.")

    return render(request, 'register.html', context)


def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main:show_main')
        else:
            messages.info(
                request, 'Sorry, incorrect username or password. Please try again.')
    context = {'form': form}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('main:login')


def search(request):
    query = request.GET.get('q')
    # Misalnya mencari produk berdasarkan nama
    results = Book.objects.filter(title__icontains=query)
    data = [{'title': books.title, 'author': books.author, 'average_rating': books.average_rating,
             'isbn': books.isbn, 'isbn13': books.isbn13, 'language_code': books.language_code, } for books in results]
    print(data)
    return JsonResponse(data, safe=False)
