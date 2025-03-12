from django.urls import path
from .views import hello_world, signup, login

urlpatterns = [
    path('hello/', hello_world),
    path("signup/", signup, name = 'signup'),
    path("login/", login, name = 'login'),
]