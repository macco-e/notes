from django.contrib import admin
from django.urls import include, path

from .views import sign_up, create_user

app_name = 'notes'
urlpatterns = [
    path('', sign_up, name='signup'),
    path('create_user/', create_user, name='create_user')
]
