from django.forms import ModelForm, Textarea
from .models import Review

class Review(ModelForm):
    class Meta:
        model = Review
        fields = ["user", "review"]
        widgets = {
            'review': Textarea(attrs={'cols': 40, 'rows': 15})
        }