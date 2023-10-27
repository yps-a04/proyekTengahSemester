from django.urls import path
from main.views import show_main, register, login_user, logout_user,search, bookmark
app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('search/', search, name='search'),
    path('b/<str:key>', bookmark, name='bookmark'),

]
