from django.contrib import admin
from django.urls import include, path

from .views import sign_up_view, create_user, login_view, HomeView, logout_view, PostNoteView, SettingsView, follow, unfollow
from .views import NoteDetailView, delete_note, NoteUpdateView, redirect_to_home
from .views import NotesView, UsersView, UserView, UserFollowView, UserFollowerView
from .views import password_change, delete_account

app_name = 'notes'
urlpatterns = [
    path('', redirect_to_home, name='redirect_to_home'),

    path('login/', login_view, name='login'),
    path('signup/', sign_up_view, name='signup'),
    path('create_user/', create_user, name='create_user'),
    path('logout/', logout_view, name='logout'),

    path('home/', HomeView.as_view(), name='home'),
    path('notes/', NotesView.as_view(), name='notes'),
    path('users/', UsersView.as_view(), name='users'),
    path('user/<int:pk>', UserView.as_view(), name='user_page'),
    path('user/<int:pk>/follow', UserFollowView.as_view(),
         name='user_follow_list'),
    path('user/<int:pk>/follower', UserFollowerView.as_view(),
         name='user_follower_list'),

    path('follow/<int:pk>', follow, name='follow'),
    path('unfollow/<int:pk>', unfollow, name='unfollow'),

    path('settings/<int:pk>', SettingsView.as_view(), name='settings'),

    path('post/', PostNoteView.as_view(), name='post_note'),

    path('note/<int:pk>', NoteDetailView.as_view(), name='note_detail'),
    path('note/edit/<int:pk>', NoteUpdateView.as_view(), name='note_update'),
    path('note/delete/<int:pk>', delete_note, name='note_delete'),

    path('password_change/', password_change, name='password_change'),
    path('delete_account/<int:pk>', delete_account, name='delete_account'),


]
