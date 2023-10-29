from django.urls import path
from bookmark.views import show_bookmark, delete_bookmark, sort_bookmark

app_name = 'bookmark'

urlpatterns = [
    path('<str:key>/', show_bookmark, name='show_bookmark'),
    path('delete/<int:key>', delete_bookmark, name="delete_bookmark"),
]

