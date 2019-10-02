from django.contrib import admin
from django.urls import include, path

from .views import sign_up_view, create_user, login_view, HomeView, logout_view, UserDetailView, PostNoteView, SettingsView, follow, unfollow, UserFollowListView, UserFollowerListView, UsersListView
from .views import UsersSearchView, search_redirect, HomeNotesSearchView, search_home_redirect, UserNoteSearchView, search_user_redirect, SearchListView
from .views import search_notes_redirect, SearchedListView, NoteDetailView, delete_note, NoteUpdateView

app_name = 'notes'
urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', sign_up_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('create_user/', create_user, name='create_user'),

    path('home/', HomeView.as_view(), name='home'),
    path('search_home_redirect/', search_home_redirect, name='search_home_redirect'),
    path('home/search/<str:search_word>', HomeNotesSearchView.as_view(), name='home_notes_search'),

    path('search/', SearchListView.as_view(), name="search"),
    path('search_notes_redirect', search_notes_redirect, name="search_notes_redirect"),
    path('search/<str:search_word>', SearchedListView.as_view(), name="searched"),

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

    path('note/<int:pk>', NoteDetailView.as_view(), name='note_detail'),
    path('note/edit/<int:pk>', NoteUpdateView.as_view(), name='note_update'),
    path('note/delete/<int:pk>', delete_note, name='note_delete'),
]
