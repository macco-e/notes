from django.contrib import admin
from django.urls import include, path

from .views import sign_up_view, create_user, login_view, HomeView, redirect_to, logout_view, UserDetailView, PostNoteView

app_name = 'notes'
urlpatterns = [
    path('', sign_up_view, name='signup'),
    path('create_user/', create_user, name='create_user'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('user/<int:pk>', UserDetailView.as_view(), name='detail'),
    path('redirect_to/', redirect_to, name='redirect_to'),
    path('create/', PostNoteView.as_view(), name='post_note'),
]
