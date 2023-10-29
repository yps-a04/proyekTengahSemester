from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from main.models import Book
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import datetime
from admin_section.models import Review


# Create your views here.


def show_book_detail(request, key):
    # Menunjukkan buku berdasarkan ID
    user = request.user
    book = Book.objects.get(pk=key)
    form = ReviewForm()
    reviews = Review.objects.all().filter(book=book)
    context = {
        'book': book,
        'form': form,
        'reviews': reviews,
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
        user = request.user
        name = request.POST.get('bookname')
        print(name)
        book = Book.objects.all().filter(title=name)

        print(book)
        title = request.POST.get("title")
        review = request.POST.get("review")

        new_rev = Review(book=book.first(), user=user,
                         review=review, title=title)
        new_rev.save()

        reviews = Review.objects.filter(book=book.first())
        data = [{'user': review.user.username, 'review': review.review, 'title': review.title}
                for review in reviews]

        return JsonResponse(data, safe=False)
    return HttpResponseNotFound()
