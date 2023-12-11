from django.urls import path
from admin_section.views import *
from book_details.views import show_book_detail
app_name = 'admin_section'

urlpatterns = [
    path('show/', show_admin, name='show_admin'),
    path('book-list-admin/', show_book_list_admin, name='show_book_list_admin'),
    path('user-list/', user_list, name='user_list'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('get-book/', get_book_json, name='get_book_json'),
    path('create-book-ajax/', add_book_ajax, name='add_book_ajax'),
    path('book-detail/<int:key>', show_book_detail, name='show_book_detail'),
    path('edit-book/<int:id>', edit_book, name='edit_book'),
    path('delete/<int:id>', delete_book, name='delete_book'),
    path('delete-flutter/<int:id>', delete_book_flutter, name='delete_book_flutter'),
    path('api/users/', get_user, name='user-list'),
    path('create-flutter/', create_book_flutter, name='create_book_flutter'),
    path('edit-flutter/<int:id>', edit_book_flutter, name='edit_book_flutter')
]
