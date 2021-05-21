from django.urls import path
from . import views

urlpatterns = [
    path('book/add_book', views.book),
    # path('register', views.addUserToDB),
    # path('login', views.loginUserToDB),
    path('book/logout', views.logout),
    path('book/addbook', views.addbook),
    path('book/<int:bookid>', views.book_click),
    # path('unlike/(<bookid>)', views.unlike_book),
    # path('like/(<bookid>)', views.like_book),
    # path('delete/(<bookid>)', views.delete_book),
    path('editbook/(<bookid>)', views.edit_book),
    
]