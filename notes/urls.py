from django.contrib import admin
from django.urls import include, path

from .views import sign_up_view, create_user, login_view, HomeView, logout_view, UserDetailView, PostNoteView, SettingsView, follow, unfollow, UserFollowListView, UserFollowerListView
from .views import UserNoteSearchView, search_user_redirect
from .views import NoteDetailView, delete_note, NoteUpdateView
from .views import NotesView, UsersView

app_name = 'notes'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', sign_up_view, name='signup'),
    path('create_user/', create_user, name='create_user'),
    path('logout/', logout_view, name='logout'),

    path('home/', HomeView.as_view(), name='home'),
    path('home/search/', HomeView.as_view(), name='home_search'),

    path('notes/', NotesView.as_view(), name='notes'),
    path('notes/search/', NotesView.as_view(), name='notes_search'),

    path('users/', UsersView.as_view(), name='users'),
    path('users/search/', UsersView.as_view(), name='users_search'),

    path('user/<int:pk>', UserDetailView.as_view(), name='detail'),
    path('user/<int:pk>/follow', UserFollowListView.as_view(), name='follow_list'),
    path('user/<int:pk>/follower', UserFollowerListView.as_view(), name='follower_list'),
    path('search_user_redirect/<int:self_pk>', search_user_redirect, name='search_user_redirect'),
    path('user/<int:self_pk>/search/<str:search_word>', UserNoteSearchView.as_view(), name='user_notes_search'),

    path('follow/<int:pk>', follow, name='follow'),
    path('unfollow/<int:pk>', unfollow, name='unfollow'),

    path('settings/<int:pk>', SettingsView.as_view(), name='settings'),

    path('create/', PostNoteView.as_view(), name='post_note'),

    path('note/<int:pk>', NoteDetailView.as_view(), name='note_detail'),
    path('note/edit/<int:pk>', NoteUpdateView.as_view(), name='note_update'),
    path('note/delete/<int:pk>', delete_note, name='note_delete'),
]
