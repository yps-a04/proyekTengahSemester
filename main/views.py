import datetime
from django.shortcuts import render, redirect
from main.models import Book
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Q

from .forms import LoginForm, SignUpForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from bookmark.models import Bookmark
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Case, When, Value, IntegerField
from profiles.models import Preference
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required
# Create your views here.


def show_main(request):

    # set pagination 50/page
    context = {
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)


@login_required(login_url='/login')
def show_book_list(request):

    page = request.GET.get('page')
    sort_param = request.GET.get('sort_by')  # Dapatkan parameter sort

    if sort_param is None:
        sort_param = ""

    if page is None:
        page = 1

    print("sort-param ===" + sort_param)

    if sort_param == 'alphabet-asc':
        books = Book.objects.order_by('title')
    elif sort_param == 'alphabet-desc':
        books = Book.objects.order_by('-title')
    elif sort_param == 'reviews-count':
        books = Book.objects.order_by('-text_review_count')
    elif sort_param == 'preference':
        author = Preference.objects.filter(user=request.user).values('author')
        books = Book.objects.none()
        sisa = Book.objects.none()
        for elem in author:
            books_temp = Book.objects.filter(author=elem['author'])
            for book in books_temp:
                books = books | books_temp
                books_all = Book.objects.all()
                for book2 in books_all:
                    if book.author in book2.author:
                        book2_query = Book.objects.filter(pk=book2.pk)
                        books = books | book2_query
    else:
        books = Book.objects.all()

    p = Paginator(books, 20)
    books = p.get_page(page)

    print('books === ' + str(books))

    context = {
        'books': books,
        'sort_param': sort_param,  # Kirim sort_param kembali ke template
    }

    return render(request, "book_list.html", context)


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
                request, "Register Failed.")

    return render(request, 'register.html', context)


def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                response = HttpResponseRedirect(reverse('admin_section:show_admin'))
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
            else:
                response = HttpResponseRedirect(reverse('main:show_main'))
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
        else:
            messages.info(
                request, 'Sorry, incorrect username or password. Please try again.')
    context = {'form': form}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


def search(request):
    query = request.GET.get('q')

    # Misalnya mencari produk berdasarkan nama
    results = Book.objects.filter(title__icontains=query)
    results = Book.objects.filter(
        Q(title__icontains=query) | Q(
            isbn__icontains=query) | Q(author__icontains=query)
    )

    if results is not None:
        data = [{'pk': books.pk, 'title': books.title, 'author': books.author, 'average_rating': books.average_rating,
                 'isbn': books.isbn, 'isbn13': books.isbn13, 'language_code': books.language_code} for books in results]
    else:
        data = 0

    return JsonResponse(data, safe=False)


def sort_books(request):
    sort_by = request.GET.get('sort_by')
    if sort_by == 'alphabet-asc':
        books = Book.objects.order_by('title')
    elif sort_by == 'alphabet-desc':
        books = Book.objects.order_by('-title')
    elif sort_by == 'reviews-count':
        books = Book.objects.order_by('-text_review_count')
    elif sort_by == 'preference':
        author = Preference.objects.filter(user=request.user).values('author')
        books = Book.objects.none()
        for book in books:
            print(book.author)
        for elem in author:
            books_temp = Book.objects.filter(author=elem['author'])
            for book in books_temp:
                print(book.author)
                books = books | books_temp
                books_all = Book.objects.all()
                for book2 in books_all:
                    if book.author in book2.author:
                        book2_query = Book.objects.filter(pk=book2.pk)
                        books = books | book2_query
    else:
        books = Book.objects.all()
    
    book_list = [{'pk': book.pk, 'title': book.title, 'author': book.author, 'average_rating': book.average_rating,
                  'isbn': book.isbn, 'isbn13': book.isbn13, 'language_code': book.language_code} for book in books[:20]]

    return JsonResponse(book_list, safe=False)
