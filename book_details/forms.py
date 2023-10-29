from django.forms import ModelForm, Textarea
from admin_section.models import Review
from django import forms


class ReviewForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'id': 'title', 'class': 'form-control active', 'type': 'text', 'placeholder': 'Title', 'style': 'height:50px;'})
    )
    review = forms.CharField(
        widget=forms.TextInput(
            attrs={'id': 'review_input', 'class': 'form-control active', 'placeholder': 'Review'})
    )
