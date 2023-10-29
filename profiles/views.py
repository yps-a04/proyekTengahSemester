from django.shortcuts import render, redirect
from main.models import Book
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from profiles.forms import *
from profiles.models import *
from bookmark.models import *
from django.core import serializers
import random
# Create your views here.
@login_required(login_url='/login')
def preference(request):
    author = Book.objects.all().values('author').exclude(author__icontains='/').distinct()
    form = DynamicCheckboxForm(request.POST or None)
    start = random.randrange(0, 50)
    first_half_fields = list(form)[start:start+8]
    second_half_fields = list(form)[start+8:start+16]
    context = {
        'author': author,
        'form':form,
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
                Preference.objects.filter(user=request.user).delete()
            else:
                return redirect('profiles:showprofile')
            for field in form.cleaned_data:
                if form.cleaned_data[field]:
                    # Assuming the field name is the author's name
                    author_name = form.fields[str(field)].label
                    preference, created = Preference.objects.get_or_create(user=request.user, author=author_name)
                    if created:
                        counter += 1
                        preference.save()
                    preferences = Preference.objects.filter(user=request.user).values('author')
            return redirect('profiles:showprofile')


    return render(request, "preference.html", context)


@login_required(login_url='/login')
def showprofile(request):
    user_now = request.user
    review = Review.objects.filter(user=user_now)
    preference = Preference.objects.filter(user=user_now)
    context = {'user':user_now, 'review':review, 'pref':preference}
    return render(request, "showprofile.html", context)

@login_required(login_url='/login')
def pref_json(request):
    preferences = Preference.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', preferences))



