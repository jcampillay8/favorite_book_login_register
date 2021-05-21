from django.urls import path
from . import views

urlpatterns = [
    path('book/add_book', views.book),
    path('book/logout', views.logout),
    path('book/addbook', views.addbook),
    path('book/<int:bookid>', views.book_click),
    path('unlike/<int:bookid>', views.unlike_book),
    path('like/<int:bookid>', views.like_book),
    path('delete/<int:bookid>', views.delete_book),
    path('editbook/<int:bookid>', views.edit_book),
    
]