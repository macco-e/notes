from django.contrib import admin
from django.urls import include, path

from .views import temp

app_name = 'notes'
urlpatterns = [
    path('', temp),
]
