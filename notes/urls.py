from django.contrib import admin
from django.urls import include, path

from .views import sign_up_view, create_user, login_view, HomeView, redirect_to

app_name = 'notes'
urlpatterns = [
    path('', sign_up_view, name='signup'),
    path('create_user/', create_user, name='create_user'),
    path('login/', login_view, name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('redirect_to/', redirect_to, name='redirect_to')
]
