from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Account, Follow, Notes


# auth -------------------------------------------------------------------------

def sign_up_view(request):
    """Renders the signup page."""
    return render(request, 'notes/signup.html')


def create_user(request):
    """Renders the home page."""
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
    """Renders the login page. If authenticated, redirect to home"""
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
    """Renders the Home page."""
    template_name = 'notes/home.html'
    context_object_name = 'notes_list'

    def get_queryset(self):
        user_id = self.request.user.id
        follows = Follow.objects.filter(follow_id=user_id)
        target_list = [str(user_id)] + [str(f.follower_id.id) for f in follows]

        if self.request.GET.get('q'):
            return Notes.objects.filter(
                noted_user_id__in=target_list,
                text__contains=self.request.GET['q']).order_by('-created_at')
        else:
            return Notes.objects.filter(
                noted_user_id__in=target_list).order_by('-created_at')

# User -------------------------------------------------------------------------

class UserDetailView(LoginRequiredMixin, ListView):
    model = Notes
    template_name = 'notes/user.html'
    context_object_name = 'notes_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_follow'] = Follow.objects.filter(follow_id=self.kwargs['pk']).count()
        context['num_follower'] = Follow.objects.filter(follower_id=self.kwargs['pk']).count()
        context['is_follow'] = Follow.objects.filter(follow_id=self.request.user.id).filter(follower_id=self.kwargs['pk']).count()
        context['target_user'] = Account.objects.get(pk=self.kwargs['pk'])
        context['notes_list'] = self.model.objects.filter(noted_user_id=self.kwargs['pk']).order_by('-created_at')
        context['self_pk'] = self.kwargs['pk']
        return context

@login_required
def follow(request, pk):
    f = Follow.objects.create(follow_id=request.user,
                              follower_id=Account.objects.get(pk=pk))
    f.save()
    return redirect('notes:detail', pk=pk)

@login_required
def unfollow(request, pk):
    f = Follow.objects.filter(follow_id=request.user).filter(follower_id=pk)
    f.delete()
    return redirect('notes:detail', pk=pk)

@login_required
def search_user_redirect(request, self_pk):
    if request.POST['search_word']:
        return redirect('notes:user_notes_search', self_pk=self_pk, search_word=request.POST['search_word'])
    else:
        return redirect('notes:detail', pk=self_pk)


class UserNoteSearchView(LoginRequiredMixin, ListView):
    model = Notes
    template_name = 'notes/user.html'
    context_object_name = 'notes_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_follow'] = Follow.objects.filter(follow_id=self.request.user.id).count()
        context['num_follower'] = Follow.objects.filter(follower_id=self.request.user.id).count()
        context['is_follow'] = Follow.objects.filter(follow_id=self.request.user.id).filter(follower_id=self.kwargs['self_pk']).count()
        context['target_user'] = Account.objects.get(pk=self.kwargs['self_pk'])
        context['notes_list'] = self.model.objects.filter(noted_user_id=self.kwargs['self_pk'], text__contains=self.kwargs['search_word']).order_by('-created_at')
        context['self_pk'] = self.kwargs['self_pk']
        return context


class UserView(LoginRequiredMixin, ListView):
    template_name = 'notes/user.html'
    # context_object_name = 'notes_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login_user = self.request.user.id
        target_user = Account.objects.get(pk=self.kwargs['pk'])

        context['target_user'] = target_user
        context['num_follow'] = Follow.objects.filter(follow_id=target_user).count()
        context['num_follower'] = Follow.objects.filter(follower_id=target_user).count()
        context['is_follow'] = Follow.objects.filter(follow_id=login_user, follower_id=target_user)
        if self.request.GET.get('q'):
            search_word = self.request.GET['q']
            context['target_user_notes_list'] = Notes.objects.filter(author=target_user, text__contains=search_word).order_by('-created_at')
        else:
            context['target_user_notes_list'] = Notes.objects.filter(author=target_user).order_by('-created_at')
        return context

# follow list ------------------------------------------------------------------

class UserFollowListView(LoginRequiredMixin, ListView):
    template_name = 'notes/follow_list.html'
    context_object_name = 'follow_list'

    def get_queryset(self):
        fs = Follow.objects.filter(follow_id=self.kwargs['pk'])
        follows = [str(f.follower_id.id) for f in fs]
        return Account.objects.filter(id__in=follows)


class UserFollowerListView(LoginRequiredMixin, ListView):
    template_name = 'notes/follower_list.html'
    context_object_name = 'follower_list'

    def get_queryset(self):
        fs = Follow.objects.filter(follower_id=self.kwargs['pk'])
        followers = [str(f.follow_id.id) for f in fs]
        return Account.objects.filter(id__in=followers)

# All notes---------------------------------------------------------------------


class NotesView(LoginRequiredMixin, ListView):
    """Renders the All notes page."""
    template_name = 'notes/all_notes.html'
    context_object_name = 'notes_list'

    def get_queryset(self):
        if self.request.GET.get('q'):
            return Notes.objects.filter(
                text__contains=self.request.GET['q']).order_by('-created_at')
        else:
            return Notes.objects.all().order_by('-created_at')


# Users ------------------------------------------------------------------------

class UsersView(LoginRequiredMixin, ListView):
    """Renders the All notes page."""
    template_name = 'notes/users.html'
    context_object_name = 'users_list'

    def get_queryset(self):
        if self.request.GET.get('q'):
            return Account.objects.filter(
                username__contains=self.request.GET['q'])
        else:
            return Account.objects.all()


# Settings----------------------------------------------------------------------

class SettingsView(LoginRequiredMixin, UpdateView):
    model = Account
    template_name = 'notes/settings.html'
    fields = ['username', 'icon']
    success_url = reverse_lazy('notes:home')


# Create -----------------------------------------------------------------------

class PostNoteView(LoginRequiredMixin, CreateView):
    model = Notes
    template_name = 'notes/post_note.html'

    fields = ['noted_user_id', 'text']
    success_url = reverse_lazy('notes:home')


# Note detail ------------------------------------------------------------------

class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Notes
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'

@login_required
def delete_note(request, pk):
    Notes.objects.get(pk=pk).delete()
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('notes:home')


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Notes
    template_name = 'notes/note_update.html'
    context_object_name = 'note'

    fields = ['noted_user_id', 'text']
    success_url = reverse_lazy('notes:home')

