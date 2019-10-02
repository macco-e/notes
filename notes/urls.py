from django.contrib import admin
from django.urls import include, path

from .views import sign_up_view, create_user, login_view, HomeView, logout_view, UserDetailView, PostNoteView, SettingsView, follow, unfollow, UserFollowListView, UserFollowerListView, UsersListView
from .views import UsersSearchView, search_redirect, HomeNotesSearchView, search_home_redirect, UserNoteSearchView, search_user_redirect

app_name = 'notes'
urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', sign_up_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('create_user/', create_user, name='create_user'),

    path('home/', HomeView.as_view(), name='home'),
    path('search_home_redirect/', search_home_redirect, name='search_home_redirect'),
    path('home/search/<str:search_word>', HomeNotesSearchView.as_view(), name='home_notes_search'),

    path('user/<int:pk>', UserDetailView.as_view(), name='detail'),
    path('user/<int:pk>/follow', UserFollowListView.as_view(), name='follow_list'),
    path('user/<int:pk>/follower', UserFollowerListView.as_view(), name='follower_list'),
    path('search_user_redirect/<int:self_pk>', search_user_redirect, name='search_user_redirect'),
    path('user/<int:self_pk>/search/<str:search_word>', UserNoteSearchView.as_view(), name='user_notes_search'),

    path('follow/<int:pk>', follow, name='follow'),
    path('unfollow/<int:pk>', unfollow, name='unfollow'),

    path('users/', UsersListView.as_view(), name='users'),
    path('search_redirect/', search_redirect, name='search_redirect'),
    path('users/search/<str:search_word>', UsersSearchView.as_view(), name='users_search'),

    path('settings/<int:pk>', SettingsView.as_view(), name='settings'),

    path('create/', PostNoteView.as_view(), name='post_note'),
]
