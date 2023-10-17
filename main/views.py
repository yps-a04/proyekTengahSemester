from django.shortcuts import render
from main.models import Book
from django.core.paginator import Paginator
# Create your views here.


def show_main(request):

    # set pagination 50/page
    p = Paginator(Book.objects.all(), 50)
    page = request.GET.get('page')

    books = p.get_page(page)
    context = {
        'books': books,
    }

    return render(request, "main.html", context)
