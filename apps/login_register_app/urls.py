from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('users/', views.users, name='users'),
    path('register', views.register, name='register'),
    path('success/(<int:id>)', views.success, name='success'),
    path('user/(<int:id>)/delete', views.delete_user, name='delete_user'),
    path('login', views.login, name="login"),
]