from django.shortcuts import render

# Create your views here.
def show_book_detail(request, key):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, "book_details.html", context)