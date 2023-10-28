from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Book
from .forms import Review
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
def show_book_detail(request, key):
    # Menunjukkan buku berdasarkan ID
    book = get_object_or_404(Book, pk=key)
    form = Review()
    context = {
        'book': book,
        'form': form,
    }

    return render(request, "book_details.html", context)

@login_required
def add_review(request, key):
    # Menambahkan review buku
    book = get_object_or_404(Book, pk=key)
    form = Review(request.POST)
    if form.is_valid():
        user = form.cleaned_data['user']
        rev = form.cleaned_data['review']

        user = request.user.username
        reviews = Review()

        reviews.book = book
        reviews.user = user
        reviews.review = rev

        reviews.date = datetime.datetime.now()
        reviews.save()

        return HttpResponseRedirect(reverse('book_details.html', args=(key)))
    
    context = {
        'book': book,
        'form': form,
    }

    return render(request, "book_details.html", context)