from django.contrib import admin
from django.urls import include, path

from .views import sign_up_view, create_user, login_view, HomeView, redirect_to, logout_view, UserDetailView, PostNoteView, SettingsView, follow, unfollow, UserFollowListView, UserFollowerListView

app_name = 'notes'
urlpatterns = [
    path('signup/', sign_up_view, name='signup'),
    path('create_user/', create_user, name='create_user'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('user/<int:pk>', UserDetailView.as_view(), name='detail'),
    path('user/<int:pk>/follow', UserFollowListView.as_view(), name='follow_list'),
    path('user/<int:pk>/follower', UserFollowerListView.as_view(), name='follower_list'),
    path('redirect_to/', redirect_to, name='redirect_to'),
    path('create/', PostNoteView.as_view(), name='post_note'),
    path('settings/<int:pk>', SettingsView.as_view(), name='settings'),
    path('follow/<int:pk>', follow, name='follow'),
    path('unfollow/<int:pk>', unfollow, name='unfollow'),
]
