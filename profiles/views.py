from django.shortcuts import render, redirect
from book.models import Book
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from profiles.forms import *
from profiles.models import *
from bookmark.models import *
from django.core import serializers
import random
from admin_section.models import *
from admin_section.models import Review
from django.contrib.auth import get_user
# Create your views here.


@login_required(login_url='/login')
def preference(request):
    author = Book.objects.all().values('author').exclude(
        author__icontains='/').distinct()
    form = DynamicCheckboxForm(request.POST or None)
    start = random.randrange(0, 50)
    first_half_fields = list(form)[start:start+8]
    second_half_fields = list(form)[start+8:start+16]
    context = {
        'author': author,
        'form': form,
        'first_half_fields': first_half_fields,
        'second_half_fields': second_half_fields
    }
    if request.method == "POST":
        counter = 0
        flag = False
        if form.is_valid():
            for field in form.cleaned_data:
                if form.cleaned_data[field] == True:
                    flag = True
                    break
            if flag == True:
                Preference.objects.filter(user=get_user(request)).delete()
            else:
                return redirect('profiles:showprofile')
            for field in form.cleaned_data:
                if form.cleaned_data[field]:
                    # Assuming the field name is the author's name
                    author_name = form.fields[str(field)].label
                    preference, created = Preference.objects.get_or_create(
                        user=get_user(request), author=author_name)
                    if created:
                        counter += 1
                        preference.save()
                    preferences = Preference.objects.filter(
                        user=get_user(request)).values('author')
            return redirect('profiles:showprofile')

    return render(request, "preference.html", context)


@login_required(login_url='/login')
def showprofile(request):
    user_now = get_user(request)
    review = Review.objects.filter(user=user_now)
    preference = Preference.objects.filter(user=user_now)
    for pref in preference:
        print(pref.author)
    context = {'user': user_now, 'review': review, 'pref': preference}
    return render(request, "showprofile.html", context)


@login_required(login_url='/login')
def pref_json(request):
    preferences = Preference.objects.filter(user=get_user(request))
    return HttpResponse(serializers.serialize('json', preferences))

@login_required(login_url='/login')
def ret_profile(request):
    user = get_user(request)
    if (user.is_superuser):
        role = "Admin"
    else:
        role = "User"

    data = {
        'user': user.username,
        'role': role,
    }

    # Return it as JSON
    return JsonResponse(data)

def ret_review(request):
    title = []
    reviewnya = []
    author = []
    reviews = Review.objects.filter(user=get_user(request))
    for elem in reviews:
        title.append(elem.title)
        reviewnya.append(elem.review)
        author.append(elem.book.author)
    return JsonResponse({'title': title, 'reviewnya': reviewnya, 'author':author})

def change_pref(request):
    author = Book.objects.all().values('author').exclude(
        author__icontains='/').distinct()
    author_list = list(author)  # Convert queryset to list
    random_authors = random.sample(author_list, 8)  # Get 8 random elements
    return JsonResponse({'author':random_authors})