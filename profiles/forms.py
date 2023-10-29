from django import forms
from main.models import Book

class DynamicCheckboxForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DynamicCheckboxForm, self).__init__(*args, **kwargs)
        queryset = Book.objects.order_by('-text_review_count').values('author').exclude(author__icontains='/').distinct()
        index = 0
        for obj in queryset:
            self.fields[str(index)] = forms.BooleanField(label=str(obj['author']), required=False)
            index += 1
            # if index == 16:
            #     break