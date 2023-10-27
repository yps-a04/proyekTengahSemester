from django.urls import path
from bookmark.views import show_bookmark

app_name = 'bookmark'

urlpatterns = [
    path('<str:key>/', show_bookmark, name='show_bookmark'),
]

