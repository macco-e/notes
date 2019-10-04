from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Account, Follow, Notes


# Auth -------------------------------------------------------------------------
@login_required
def redirect_to_home(request):
    return redirect('notes:home')


def sign_up_view(request):
    return render(request, 'notes/signup.html')


def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            Account.objects.create_user(username, password=password)
            return redirect('notes:login')
        except IntegrityError:
            return redirect('notes:signup')

    if request.method == 'GET':
        return redirect('notes:signup')


def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('notes:home')
        else:
            return render(request, 'notes/login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('notes:home')
        else:
            return render(request, 'notes/login.html',
                          {'error': 'ユーザ名かパスワードが間違っています'})


def logout_view(request):
    logout(request)
    return redirect('notes:login')


# Home--------------------------------------------------------------------------

class HomeView(LoginRequiredMixin, ListView):
    template_name = 'notes/home.html'
    context_object_name = 'notes_list'

    def get_queryset(self):
        user_id = self.request.user.id
        follows = Follow.objects.filter(follow=user_id)
        follow_list = [str(user_id)] + [str(f.follower.id) for f in follows]

        if self.request.GET.get('q'):
            return Notes.objects.filter(
                author__in=follow_list,
                text__contains=self.request.GET['q']).order_by('-created_at')
        else:
            return Notes.objects.filter(
                author__in=follow_list).order_by('-created_at')


# All notes---------------------------------------------------------------------

class NotesView(LoginRequiredMixin, ListView):
    template_name = 'notes/all_notes.html'
    context_object_name = 'notes_list'

    def get_queryset(self):
        if self.request.GET.get('q'):
            search_word = self.request.GET['q']
            return Notes.objects.filter(
                text__contains=search_word).order_by('-created_at')
        else:
            return Notes.objects.all().order_by('-created_at')


# Note  ------------------------------------------------------------------

class PostNoteView(LoginRequiredMixin, CreateView):
    model = Notes
    template_name = 'notes/post_note.html'

    fields = ['author', 'text']
    success_url = reverse_lazy('notes:home')


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Notes
    template_name = 'notes/note_update.html'
    context_object_name = 'note'

    fields = ['author', 'text']
    success_url = reverse_lazy('notes:home')


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Notes
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'


@login_required
def delete_note(request, pk):
    Notes.objects.get(pk=pk).delete()
    return redirect('notes:home')


# Users ------------------------------------------------------------------------

class UsersView(LoginRequiredMixin, ListView):
    template_name = 'notes/users.html'
    context_object_name = 'users_list'

    def get_queryset(self):
        if self.request.GET.get('q'):
            return Account.objects.filter(
                username__contains=self.request.GET['q'])
        else:
            return Account.objects.all()


# User -------------------------------------------------------------------------

class UserView(LoginRequiredMixin, ListView):
    model = Notes
    template_name = 'notes/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login_user = self.request.user.id
        target_user = Account.objects.get(pk=self.kwargs['pk'])

        context['target_user'] = target_user
        context['num_follow'] = Follow.objects.filter(
            follow=target_user).count()
        context['num_follower'] = Follow.objects.filter(
            follower=target_user).count()

        context['is_follow'] = bool(Follow.objects.filter(follow=login_user,
                                                     follower=target_user).count())
        if self.request.GET.get('q'):
            search_word = self.request.GET['q']
            context['target_user_notes_list'] = Notes.objects.filter(
                author=target_user,
                text__contains=search_word).order_by('-created_at')
        else:
            context['target_user_notes_list'] = Notes.objects.filter(
                author=target_user).order_by('-created_at')
        return context


# Relation ---------------------------------------------------------------------

class UserRelationshipView(LoginRequiredMixin, ListView):
    template_name = 'notes/user_relationship.html'
    context_object_name = 'accounts_list'

    def get_queryset(self):
        path = self.request.path
        relation = path.split('/')[-1]

        if relation == 'follow':
            # Render follow list
            follows_obj = Follow.objects.filter(follow=self.kwargs['pk'])
            follows_pk = [str(follow_obj.follower.pk) for follow_obj in follows_obj]

            if self.request.GET.get('q'):
                # render searched follow list
                search_word = self.request.GET['q']
                return Account.objects.filter(pk__in=follows_pk,
                                              username__contains=search_word)
            else:
                return Account.objects.filter(pk__in=follows_pk)

        if relation == 'follower':
            # Render follower list
            followers_obj = Follow.objects.filter(follower=self.kwargs['pk'])
            followers_pk = [str(follower_obj.follow.pk) for follower_obj in followers_obj]

            if self.request.GET.get('q'):
                # Render searched follower list
                search_word = self.request.GET['q']
                return Account.objects.filter(pk__in=followers_pk,
                                              username__contains=search_word)
            else:
                return Account.objects.filter(pk__in=followers_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['relation'] = self.request.path.split('/')[-1]
        return context


@login_required
def follow(request, pk):
    f = Follow.objects.create(follow=request.user,
                              follower=Account.objects.get(pk=pk))
    f.save()
    return redirect('notes:user_page', pk=pk)


@login_required
def unfollow(request, pk):
    f = Follow.objects.filter(follow=request.user).filter(follower=pk)
    f.delete()
    return redirect('notes:user_page', pk=pk)


# Settings----------------------------------------------------------------------

class SettingsView(LoginRequiredMixin, UpdateView):
    model = Account
    template_name = 'notes/settings.html'
    fields = ['username', 'icon']
    success_url = reverse_lazy('notes:home')
