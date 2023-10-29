from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from main.models import Book
from .forms import Review
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
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

# Get JSON dengan HttpResponse serializers
def get_reviews_json(request):
    reviews = Review.objects.all()
    return HttpResponse(serializers.serialize("json", reviews))


@csrf_exempt
# Add review dengan ajax
def add_review_ajax(request):
    if request.method == 'POST':
        book = request.POST.get("book")
        user = request.POST.get("user")
        review = request.POST.get("review")
        date = request.POST.get("date")

        new_rev = Review(book=book, user=user, review=review, date=date)
        new_rev.save()

        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()